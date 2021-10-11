from collections import defaultdict


from lib_bgp_simulator import PrefixHijack, SubprefixHijack, NonRoutedPrefixHijack
from lib_bgp_simulator import SuperprefixPrefixHijack, NonRoutedSuperprefixHijack

from .rovpp_attack import ROVPPAttack


# NOTE: Any ROV++ atk that has more than two announcements will break hole counting mechanism
# This must be fixed for later


class ROVPPSubprefixHijack(ROVPPAttack, SubprefixHijack):
    """Subprefix hijack with ROV++ ann class"""

    def count_holes(self, policy_self):
        shallow_invalid_anns = []
        neighbor_victim_prefix_dict = defaultdict(list)
        for ann in policy_self._recv_q._info[self.victim_prefix]:
            # as path index 0 because this is a shallow announcement
            # 0th in the path is the neighbor since we are pulling 
            # from the neighbors local rib
            ann.temp_holes = []
            neighbor_victim_prefix_dict[ann.as_path[0]].append(ann)

        # FIX _info IN ALL PLACES
        for ann in policy_self._recv_q._info[self.attacker_prefix]:
            victim_anns = neighbor_victim_prefix_dict.get(ann.as_path[0], [])
            for victim_ann in victim_anns:
                victim_ann.temp_holes.append(ann)
                shallow_invalid_anns.append(ann)

        for ann in policy_self._recv_q._info[self.victim_prefix]:
            # as path index 0 because this is a shallow announcement
            # 0th in the path is the neighbor since we are pulling 
            # from the neighbors local rib
            ann.temp_holes = tuple(ann.temp_holes)

        if shallow_invalid_anns:
            return {self.attacker_prefix: shallow_invalid_anns}
        else:
            return {}

    def remove_temp_holes(self, policy_self):

        # Transfer over holes for those in local rib
        victim_pref_ann = policy_self._local_rib.get_ann(self.victim_prefix)
        if victim_pref_ann is not None:
            victim_pref_ann.holes = victim_pref_ann.temp_holes
            victim_pref_ann.temp_holes = None

        # Remove holes for all those not in the local rib
        for ann in policy_self._recv_q._info[self.victim_prefix]:
            ann.temp_holes = None

class NoSubprefixesROVPPAttack(ROVPPAttack):
    def count_holes(*args, **kwargs):
        pass
    def remove_temp_holes(*args, **kwargs):
        pass

class ROVPPPrefixHijack(NoSubprefixesROVPPAttack, PrefixHijack):
    """Prefix hijack with ROV++ ann class"""

    pass

class ROVPPNonRoutedPrefixHijack(NoSubprefixesROVPPAttack, NonRoutedPrefixHijack):
    """NonRouted Prefix hijack with ROV++ ann class"""

    pass

class ROVPPNonRoutedSuperprefixHijack(ROVPPAttack, NonRoutedSuperprefixHijack):
    """NonRouted Prefix hijack with ROV++ ann class"""

    pass

class ROVPPSuperprefixPrefixHijack(ROVPPAttack, SuperprefixPrefixHijack):
    """NonRouted Prefix hijack with ROV++ ann class"""

    pass
