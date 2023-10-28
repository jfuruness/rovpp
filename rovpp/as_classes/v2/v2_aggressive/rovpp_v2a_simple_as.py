from .rovpp_v2a_lite_simple_as import ROVPPV2aLiteSimpleAS
from ...non_lite import NonLite


class ROVPPV2aSimpleAS(NonLite, ROVPPV2aLiteSimpleAS):
    name = "ROV++V2a Simple"
