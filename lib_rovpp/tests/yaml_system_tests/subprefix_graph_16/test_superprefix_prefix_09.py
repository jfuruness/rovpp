from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, ROVSimpleAS, Graph016

from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubPrefix02Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph016
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (12, )


class Test052SubprefixPrefix02(BaseSubPrefix02Tester):
    AdoptASCls = ROVSimpleAS

class Test053SubprefixPrefix02(BaseSubPrefix02Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test054SubprefixPrefix02(BaseSubPrefix02Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test055SubprefixPrefix02(BaseSubPrefix02Tester):
    AdoptASCls = ROVPPV2aSimpleAS

