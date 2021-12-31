from abc import abstractmethod

from .rovpp_ann import ROVPPAnn

class ROVPPEngineInput:
    AnnCls = ROVPPAnn

    def _get_announcements(self, **extra_ann_kwargs):
        return super()._get_announcements(preventive=False,
                                          attacker_on_route=False,
                                          blackhole=False,
                                          holes=tuple(),
                                          **extra_ann_kwargs)
