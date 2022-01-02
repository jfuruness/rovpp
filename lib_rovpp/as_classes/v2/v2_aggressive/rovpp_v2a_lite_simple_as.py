from .rovpp_v2a_simple_as import ROVPPV2aSimpleAS
from ...lite import Lite


class ROVPPV2aLiteSimpleAS(Lite, ROVPPV2aSimpleAS):

    __slots__ = []

    name = "ROV++V2a Lite Simple"
