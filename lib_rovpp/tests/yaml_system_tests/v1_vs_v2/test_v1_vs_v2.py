from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, Graph009

from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseROVPPV1vsV2Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph009
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (2, 5, 4, 1, )  # Do I need to add the victim here?


class Test018V1versus(BaseROVPPV1vsV2Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test019V2versus(BaseROVPPV1vsV2Tester):
    AdoptASCls = ROVPPV2SimpleAS

