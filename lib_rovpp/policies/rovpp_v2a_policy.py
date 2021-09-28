from .rovpp_v2a_lite_policy import ROVPPV2aLitePolicy

class ROVPPV2aPolicy(ROVPPV2aLitePolicy):

    name = "ROV++V2a"

    from .lite_converter import _new_ann_is_better, _best_by_hole_size
