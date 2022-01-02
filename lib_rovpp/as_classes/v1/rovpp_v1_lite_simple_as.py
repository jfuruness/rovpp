from .rovpp_v1_simple_as import ROVPPV1SimpleAS
from ..lite import Lite


class ROVPPV1LiteSimpleAS(Lite, ROVPPV1SimpleAS):

    name = "ROV++V1 Lite Simple"

    __slots__ = tuple()
