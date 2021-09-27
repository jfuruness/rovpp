from .rovpp_v1_lite_policy import ROVPPV1LitePolicy

class ROVPPV1Policy(ROVPPV1LitePolicy):

    name = "ROV++V1"

    from .lite_converter import _new_ann_is_better, _best_by_hole_size
