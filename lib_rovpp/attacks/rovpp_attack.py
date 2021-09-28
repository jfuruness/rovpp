from abc import abstractmethod

from .rovpp_ann import ROVPPAnn

class ROVPPAttack:
    AnnCls = ROVPPAnn

    @abstractmethod    
    def count_holes(self, policy_self):
        pass

    @abstractmethod    
    def remove_temp_holes(self, policy_self):
        pass
