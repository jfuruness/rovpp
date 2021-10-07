from .rovpp_v2_lite_policy import ROVPPV2LitePolicy

class ROVPPV2Policy(ROVPPV2LitePolicy):

    name = "ROV++V2"

    from .lite_converter import _new_ann_is_better, _new_hole_size_is_smaller
