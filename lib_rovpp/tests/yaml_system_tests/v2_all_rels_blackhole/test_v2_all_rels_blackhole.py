from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, Graph008


from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....as_classes import ROVPPV2LiteSimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseROVPPV2CustomerBlackholeTester(BaseGraphSystemTester):
    GraphInfoCls = Graph008
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (1,)


class Test014V2CustomerBlackhole(BaseROVPPV2CustomerBlackholeTester):
    AdoptASCls = ROVPPV2SimpleAS

class Test015V2LiteCustomerBlackhole(BaseROVPPV2CustomerBlackholeTester):
    AdoptASCls = ROVPPV2LiteSimpleAS

class Test016V2aCustomerBlackhole(BaseROVPPV2CustomerBlackholeTester):
    AdoptASCls = ROVPPV2aSimpleAS

class Test017V2aLiteCustomerBlackhole(BaseROVPPV2CustomerBlackholeTester):
    AdoptASCls = ROVPPV2aLiteSimpleAS
