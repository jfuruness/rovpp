from .rovpp_v2_policy import ROVPPV2Policy

class ROVPPV3Policy(ROVPPV2Policy):

    name = "ROV++V3"

    __slots__ = []

    from .lite_converter import _new_ann_better, _new_holes_smaller
