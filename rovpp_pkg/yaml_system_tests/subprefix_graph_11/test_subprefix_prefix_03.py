from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester, BGPSimpleAS, ROVSimpleAS, Graph011

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubPrefix01Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph011
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (5, 6, 1, 11, 12)


class Test017SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVSimpleAS

class Test018SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test019SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test020SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV2aSimpleAS

