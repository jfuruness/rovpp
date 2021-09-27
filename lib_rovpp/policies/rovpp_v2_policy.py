from .rovpp_v2_lite_policy import ROVPPV2LitePolicy

class ROVPPV2Policy(ROVPPV2LitePolicy):

    name = "ROV++V2"

    from .lite_converter import _new_ann_is_better, _best_by_hole_size
