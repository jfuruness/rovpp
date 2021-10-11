from copy import deepcopy
from collections import defaultdict

from ipaddress import ip_network

from lib_bgp_simulator import BGPAS, ROAValidity, ROVAS, Relationships

# subnet_of is python 3.7, not supporrted by pypy yet 
def subnet_of(self, other):
    return self in list(other.subnets) + [other]


class ROVPPV1LitePolicy(ROVAS):

    name = "ROV++V1 Lite"

    __slots__ = []

    def _policy_propagate(self, neighbor, ann, *args):
        """Only propagate announcements that aren't blackholes"""

        # Policy handled this ann for propagation (and did nothing)
        return ann.blackhole

    def process_incoming_anns(self,
                              recv_relationship,
                              propagation_round=None,
                              attack=None,
                              reset_q=True,
                              **kwargs):
        """Process all announcements that were incoming from a specific rel"""

        # Holes are invalid subprefixes from the same neighbor
        # We do this here so that we can optimize it
        # Or else it is much too slow to have a generalized version
        # See ROVPP_v1_Lite_slow, it has like 5+ nested for loops

        # Modifies the temp_holes in shallow_anns and returns prefix: blackhole_list dict
        shallow_blackholes = attack.count_holes(self)

        super(ROVPPV1LitePolicy, self).process_incoming_anns(recv_relationship,
                                                             propagation_round=propagation_round,
                                                             attack=attack,
                                                             reset_q=False,
                                                             **kwargs)

        self._get_and_assign_blackholes(shallow_blackholes, recv_relationship)

        attack.remove_temp_holes(self)
        # Move holes from temp_holes and resets q
        self._reset_q(reset_q)


##############
# Blackholes #
##############

    def _get_and_assign_blackholes(self, shallow_blackholes_dict, recv_relationship):
        """Gets blackholes and assigns them"""

        # For any announcement we have that has blackholes
        # TODO fix _info

        blackholes = []
        for ann in self._local_rib._info.values():
            if ann.temp_holes is not None:
                # For every hole/invalid_subprefix
                for invalid_subprefix_ann in ann.temp_holes:
                    #assert isinstance(invalid_subprefix_ann, ROVPPAnn)

                    # Make hole and add to RIB
                    bhole = self._copy_and_process(invalid_subprefix_ann,
                                                   recv_relationship,
                                                   blackhole=True,
                                                   traceback_end=True)
                    blackholes.append(bhole)
        # must be done this way so dict doesn't change size during iteratoin
        for blackhole in blackholes:
            self._local_rib.add_ann(blackhole)
