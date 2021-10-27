from .base_rovpp_fig3_tester import BaseROVPPFig3Tester


from ....as_classes import ROVPPV2LiteSimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS
from ....as_classes import ROVPPV2aSimpleAS

class BaseROVPPFig3V2Tester(BaseROVPPFig3Tester):
    adopting_asns = (77, 33,)
    rov_adopting_asns = (32,)


class Test005Fig3V2Lite(BaseROVPPFig3V2Tester):
    AdoptASCls = ROVPPV2LiteSimpleAS

class Test006Fig3V2(BaseROVPPFig3V2Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test007Fig3V2aLite(BaseROVPPFig3V2Tester):
    AdoptASCls = ROVPPV2aLiteSimpleAS

class Test008Fig3V2a(BaseROVPPFig3V2Tester):
    AdoptASCls = ROVPPV2aSimpleAS
