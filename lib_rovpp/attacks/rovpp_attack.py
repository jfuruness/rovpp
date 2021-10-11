from abc import abstractmethod

from .rovpp_ann import ROVPPAnn

class ROVPPAttack:
    AnnCls = ROVPPAnn

    def __init__(self, *args, **kwargs):
        super(ROVPPAttack, self).__init__(*args, blackhole=False, holes=[], temp_holes=None, **kwargs)

    @abstractmethod    
    def count_holes(self, policy_self):
        pass

    @abstractmethod    
    def remove_temp_holes(self, policy_self):
        pass
