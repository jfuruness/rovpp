from .rovpp_v2_lite_policy import ROVPPV2LitePolicy

class ROVPPV2Policy(ROVPPV2LitePolicy):

    name = "ROV++V2"

    __slots__ = []

    from .lite_converter import _new_ann_better, _new_holes_smaller
