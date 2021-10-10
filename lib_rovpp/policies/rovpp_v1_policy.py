from .rovpp_v1_lite_policy import ROVPPV1LitePolicy

class ROVPPV1Policy(ROVPPV1LitePolicy):

    name = "ROV++V1"

    __slots__ = []

    from .lite_converter import _new_ann_better, _new_holes_smaller
