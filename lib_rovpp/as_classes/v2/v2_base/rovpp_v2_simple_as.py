from .rovpp_v2_lite_simple_as import ROVPPV2LiteSimpleAS
from ...non_lite import NonLite

class ROVPPV2SimpleAS(NonLite, ROVPPV2LiteSimpleAS):

    name = "ROV++V2 Simple"

    __slots__ = []
