from lib_bgp_simulator import PrefixHijack, SubprefixHijack, UnannouncedPrefixHijack

from .rovpp_attack import ROVPPAttack


# NOTE: Any ROV++ atk that has more than two announcements will break hole counting mechanism
# This must be fixed for later


class ROVPPPrefixHijack(ROVPPAttack, PrefixHijack):
    """Prefix hijack with ROV++ ann class"""

    def count_holes(*args, **kwargs):
        pass
    def remove_temp_holes(*args, **kwargs):
        pass

class ROVPPSubprefixHijack(ROVPPAttack, SubprefixHijack):
    """Subprefix hijack with ROV++ ann class"""

    def count_holes(self, policy_self):
        shallow_invalid_anns = []
        for neighbor, prefix_ann_dict in policy_self.recv_q.items():
            victim_anns = prefix_ann_dict.get(self.victim_prefix, tuple())
            temp_holes = prefix_ann_dict.get(self.attacker_prefix, tuple())
            for victim_ann in victim_anns:
                victim_ann.temp_holes = temp_holes
                shallow_invalid_anns.extend(temp_holes)
        if shallow_invalid_anns:
            return {self.attacker_prefix: shallow_invalid_anns}
        else:
            return {}

    def remove_temp_holes(self, policy_self):

        # Transfer over holes for those in local rib
        victim_pref_ann = policy_self.local_rib.get(self.victim_prefix)
        if victim_pref_ann is not None and hasattr(victim_pref_ann, "temp_holes"):
            victim_pref_ann.holes = victim_prefix_ann.temp_holes
            del victim_prefix_ann.temp_holes

        # Remove holes for all those not in the local rib
        for neighbor, prefix_ann_dict in policy_self.recv_q.items():
            for ann in prefix_ann_dict[self.victim_prefix]:
                if hasattr(ann, "temp_holes"):
                    del ann.temp_holes
           
class ROVPPUnannouncedPrefixHijack(ROVPPAttack, UnannouncedPrefixHijack):
    """Unannounced Prefix hijack with ROV++ ann class"""

    def count_holes(*args, **kwargs):
        pass
    def remove_temp_holes(*args, **kwargs):
        pass
