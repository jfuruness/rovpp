from .base_rovpp_fig3_tester import BaseROVPPFig3Tester

from ....as_classes import ROVPPV1LiteSimpleAS, ROVPPV1SimpleAS

class BaseROVPPFig3V1Tester(BaseROVPPFig3Tester):
    adopting_asns = (77,)
    rov_adopting_asns = (32, 33,)


class Test003Fig3V1Lite(BaseROVPPFig3V1Tester):
    AdoptASCls = ROVPPV1LiteSimpleAS

class Test004Fig3V1(BaseROVPPFig3V1Tester):
    AdoptASCls = ROVPPV1SimpleAS
