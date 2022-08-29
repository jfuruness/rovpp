from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester, BGPSimpleAS, Graph008

from ..unstable import Unstable
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....as_classes import ROVPPV2LiteSimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseROVPPV2CustomerBlackholeTester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph008
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (1,)


class Test071V2CustomerBlackhole(BaseROVPPV2CustomerBlackholeTester):
    AdoptASCls = ROVPPV2SimpleAS


class Test072V2LiteCustomerBlackhole(BaseROVPPV2CustomerBlackholeTester):
    AdoptASCls = ROVPPV2LiteSimpleAS


class Test073V2aCustomerBlackhole(BaseROVPPV2CustomerBlackholeTester):
    AdoptASCls = ROVPPV2aSimpleAS


class Test074V2aLiteCustomerBlackhole(BaseROVPPV2CustomerBlackholeTester):
    AdoptASCls = ROVPPV2aLiteSimpleAS
