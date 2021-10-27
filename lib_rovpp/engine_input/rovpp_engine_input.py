from abc import abstractmethod

from .rovpp_ann import ROVPPAnn

class ROVPPEngineInput:
    AnnCls = ROVPPAnn

    def _get_announcements(self, **extra_ann_kwargs):
        return super()._get_announcements(preventive=False,
                                          attacker_on_route=False,
                                          blackhole=False,
                                          temp_holes=None,
                                          holes=tuple(),
                                          **extra_ann_kwargs)

    def count_holes(self, as_obj):
        assert self._validate_no_invalid_subprefixes(as_obj), "count_holes was not defined"

    def remove_temp_holes(self, as_obj):
        assert self._validate_no_invalid_subprefixes(as_obj), "remove_temp_holes was not defined"

    def _validate_no_invalid_subprefixes(self, as_obj):
        for prefix, ann in as_obj._recv_q.prefix_anns():
            if len(self.prefix_subprefix_dict[prefix]) != 0:
                return False
        return True
