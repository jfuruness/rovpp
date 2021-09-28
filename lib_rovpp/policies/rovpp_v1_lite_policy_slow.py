from copy import deepcopy
from collections import defaultdict

from ipaddress import ip_network

from lib_bgp_simulator import BGPPolicy, ROAValidity, ROVPolicy, Relationships

# subnet_of is python 3.7, not supporrted by pypy yet 
def subnet_of(self, other):
    return self in list(other.subnets) + [other]


class ROVPPV1LitePolicy(ROVPolicy):

    name = "ROV++V1 Lite"

    def _policy_propagate(policy_self, self, propagate_to, send_rels, ann, *args):
        """Only propagate announcements that aren't blackholes"""

        # Policy handled this ann for propagation (and did nothing)
        return ann.blackhole

    def process_incoming_anns(policy_self, self, recv_relationship, reset_q=True):
        """Process all announcements that were incoming from a specific rel"""

        # NOTE: check if this is actually faster with a double for loop instead
        prefix_subprefix_dict = policy_self._get_prefix_subprefixes()

        # Must deep copy before holes are counted
        for neighbor, prefix_ann_dict in policy_self.recv_q.items():
            for prefix, ann_list in prefix_ann_dict.items():
                copied_anns = [x.copy() for x in ann_list]
                ann_list.clear()
                ann_list.extend(copied_anns)

        # Holes are invalid subprefixes from the same neighbor
        policy_self._count_holes(prefix_subprefix_dict)

        super(ROVPPV1LitePolicy, policy_self).process_incoming_anns(self,
                                                                    recv_relationship,
                                                                    reset_q=False)

        policy_self._get_and_assign_blackholes(self)
        policy_self._reset_q(reset_q)

    def _get_prefix_subprefixes(policy_self):
        prefixes = set([])
        for ann in policy_self.recv_q.announcements:
            prefixes.add(ann.prefix)
        # Do this here for speed
        prefixes = [ip_network(x) for x in prefixes]

        for prefix in prefixes:
            # Supported in python3.7, not by pypy yet
            def subnet_of(other):
                return str(prefix) in [str(x) for x in other.subnets()] + [str(other)]
            prefix.subnet_of = subnet_of

        prefix_subprefix_dict = {x: [] for x in prefixes}
        for outer_prefix, subprefix_list in prefix_subprefix_dict.items():
            for prefix in prefixes:
                if prefix.subnet_of(outer_prefix):
                    subprefix_list.append(str(prefix))
        # Get rid of ip_network
        return {str(k): v for k, v in prefix_subprefix_dict.items()}

    def _count_holes(policy_self, prefix_subprefix_dict):
        """For each ann, get the number of invalid subprefixes from same neighbor"""

        for neighbor, prefix_ann_dict in policy_self.recv_q.items():
            for prefix, subprefix_list in prefix_subprefix_dict.items():
                anns = prefix_ann_dict.get(prefix, [])
                for ann in anns:
                    for subprefix in subprefix_list:
                        subprefix_anns = prefix_ann_dict.get(subprefix)
                        for subprefix_ann in subprefix_anns:
                            if subprefix_ann is not None and subprefix_ann.roa_validity == ROAValidity.INVALID:
                                ann.holes.append(subprefix_ann)

    def _new_ann_is_better(policy_self, self, deep_ann, shallow_ann, recv_relationship: Relationships, processed=False):
        """Assigns the priority to an announcement according to Gao Rexford"""

        # If old ann is blackhole, override with valid ann
        # NOTE that shallow ann are always valid
        if deep_ann is None or (deep_ann.blackhole and not shallow_ann.blackhole):
            return True

        return super(ROVPPV1LitePolicy, policy_self)._new_ann_is_better(self, deep_ann, shallow_ann, recv_relationship, processed=processed)

##############
# Blackholes #
##############

    def _get_and_assign_blackholes(policy_self, self):
        """Gets blackholes and assigns them"""

        blackholes_dict = defaultdict(list)
        # Below this deals with getting holes and assigning blackholes
        for prefix, ann in policy_self.local_rib.items():
            for invalid_ann in ann.holes:
                blackholes_dict[invalid_ann.prefix].append(invalid_ann)

        for prefix, blackhole_list in blackholes_dict.items():
            best_blackhole = None
            for blackhole in blackhole_list:
                if policy_self_new_ann_is_better(self, best_blackhole, blackhole, None, processed=True):
                    best_blackhole = blackhole
            assert best_blackhole is not None, "List should never be length zero"

            policy_self.local_rib[best_blackhole.prefix] = best_blackhole.copy(blackhole=True, traceback_end=True)
