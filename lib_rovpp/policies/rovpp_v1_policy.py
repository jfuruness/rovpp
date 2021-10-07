from .rovpp_v1_lite_policy import ROVPPV1LitePolicy

class ROVPPV1Policy(ROVPPV1LitePolicy):

    name = "ROV++V1"

    from .lite_converter import _new_ann_is_better, _new_hole_size_is_smaller
