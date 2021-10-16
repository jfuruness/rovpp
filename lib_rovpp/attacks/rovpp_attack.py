from abc import abstractmethod

from .rovpp_ann import ROVPPAnn

class ROVPPAttack:
    AnnCls = ROVPPAnn

    def _get_announcements(self, **extra_ann_kwargs):
        return super()._get_announcements(preventive=False,
                                          attacker_on_route=False,
                                          blackhole=False,
                                          temp_holes=None,
                                          holes=[],
                                          **extra_ann_kwargs)

    @abstractmethod    
    def count_holes(self, policy_self):
        pass

    @abstractmethod    
    def remove_temp_holes(self, policy_self):
        pass
