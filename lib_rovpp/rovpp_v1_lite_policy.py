from copy import deepcopy

from ipaddress import ip_network

from lib_bgp_simulator import BGPPolicy, IncomingAnns, ROAValidity, ROVPolicy, Relationships

from .blackhole import Blackhole


class ROVPPV1LitePolicy(ROVPolicy):

    name = "ROV++V1 Lite"

    def _policy_propagate(policy_self, self, propagate_to, send_rels, ann, as_obj):
        """Only propagate announcements that aren't blackholes"""

        # Policy handled this ann for propagation (and did nothing)
        return isinstance(ann, Blackhole)

    def process_incoming_anns(policy_self, self, recv_relationship, reset_q=True):
        """Process all announcements that were incoming from a specific rel"""


        super(ROVPPV1LitePolicy, policy_self).process_incoming_anns(self,
                                                                    recv_relationship,
                                                                    reset_q=False)

        policy_self._get_and_assign_blackholes(self)
        policy_self._reset_q(reset_q)


    def _new_ann_is_better(policy_self, self, deep_ann, shallow_ann, recv_relationship: Relationships):
        """Assigns the priority to an announcement according to Gao Rexford"""


        # If old ann is blackhole, override with valid ann
        # NOTE that shallow ann are always valid
        if isinstance(deep_ann, Blackhole) and not isinstance(shallow_ann, Blackhole):
            return True

        return super(ROVPPV1LitePolicy, policy_self)._new_ann_is_better(self, deep_ann, shallow_ann, recv_relationship)

##############
# Blackholes #
##############

    def _get_and_assign_blackholes(policy_self, self):
        """Gets blackholes and assigns them"""

        blackholes = []
        # Below this deals with getting holes and assigning blackholes
        for prefix, ann in policy_self.local_rib.items():
            # I know this is slightly slower
            # But it is negligable, esp. cause most atks will only have 2-3 prefixes
            for subprefix in policy_self._get_incoming_subprefixes(prefix):
                if policy_self._recv_invalid_ann(subprefix):
                    # You only blackhole the subprefix 

                    blackholes.append(policy_self._create_blackhole(self, ann, subprefix))
                    break

        # Must do here or else we change dict as we iterate. Big no no
        for blackhole in blackholes:
            policy_self.local_rib[blackhole.prefix] = blackhole

    def _get_incoming_subprefixes(policy_self, og_prefix):
        """Returns all prefixes in the local rib that are a subprefix of prefix"""

        ip_network_og_prefix = ip_network(og_prefix)

        for prefix in policy_self.incoming_anns:
            if ip_network(prefix).subnet_of(ip_network_og_prefix):
                yield prefix

    def _recv_invalid_ann(policy_self, subprefix):
        """Returns True if there was an invalid announcement recieved for the subprefix"""

        for ann in policy_self.incoming_anns[subprefix]:
            if ann.roa_validity == ROAValidity.INVALID:
                return True
        return False

    def _create_blackhole(policy_self, self, ann, subprefix):
        """Creates a blackhole for that announcement"""

        # NOTE: later change this to _deep_copy_ann but with blackhole set to true
        # Since you will have a customer ann class
        return Blackhole(prefix=subprefix, timestamp=ann.timestamp, as_path=(self.asn,),
                         seed_asn=self.asn, roa_validity=ROAValidity.INVALID)
