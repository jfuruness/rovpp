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

    def process_incoming_anns(policy_self, self, recv_relationship, propagation_round=None, attack=None, reset_q=True, **kwargs):
        """Process all announcements that were incoming from a specific rel"""

        # Holes are invalid subprefixes from the same neighbor
        # We do this here so that we can optimize it
        # Or else it is much too slow to have a generalized version
        # See ROVPP_v1_Lite_slow, it has like 5+ nested for loops

        # Modifies the temp_holes in shallow_anns and returns prefix: blackhole_list dict
        shallow_blackholes = attack.count_holes(policy_self)

        super(ROVPPV1LitePolicy, policy_self).process_incoming_anns(self,
                                                                    recv_relationship,
                                                                    reset_q=False)

        policy_self._get_and_assign_blackholes(self, shallow_blackholes, propagation_round)


        attack.remove_temp_holes(policy_self)
        # Move holes from temp_holes and resets q
        policy_self._reset_q(reset_q)


##############
# Blackholes #
##############

    def _get_and_assign_blackholes(policy_self, self, shallow_blackholes_dict, propagation_round):
        """Gets blackholes and assigns them"""

        # For any announcement we have that has blackholes
        # TODO fix _info
        for ann in policy_self.local_rib._info.values():
            if hasattr(ann, "temp_holes"):
                # For every hole/invalid_subprefix
                for invalid_subprefix_ann in ann.temp_holes:
                    assert isinstance(invalid_subprefix_ann, ROVPPAnn)

                    # Make hole and add to RIB
                    blackhole = invalid_subprefix_ann.copy(blackhole=True,
                                                           traceback_end=True)
                    self.local_rib.add_ann(blackhole)
