from .rovpp_v2a_lite_policy import ROVPPV2aLitePolicy

class ROVPPV2aPolicy(ROVPPV2aLitePolicy):

    __slots__ = []

    name = "ROV++V2a"

    from .lite_converter import _new_ann_better, _new_holes_smaller
