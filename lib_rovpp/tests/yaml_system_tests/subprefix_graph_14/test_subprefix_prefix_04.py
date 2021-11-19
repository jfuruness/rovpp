from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, ROVSimpleAS, Graph014

from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubPrefix01Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph014
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (6, )


class Test052SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVSimpleAS

class Test053SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test054SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test055SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV2aSimpleAS

