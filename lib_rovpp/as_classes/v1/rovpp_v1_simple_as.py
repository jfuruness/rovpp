from .rovpp_v1_lite_simple_as import ROVPPV1LiteSimpleAS
from ..non_lite import NonLite

raise NotImplementedError("Not proper non lite usage")
class ROVPPV1SimpleAS(NonLite, ROVPPV1LiteSimpleAS):

    name = "ROV++V1 Simple"

    __slots__ = []
