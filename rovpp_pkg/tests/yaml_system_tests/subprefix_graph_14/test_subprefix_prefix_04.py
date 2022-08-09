from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester
from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import Graph014

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubPrefix01Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph014
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (6, )


class Test025SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVSimpleAS


class Test026SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test027SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test028SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV2aSimpleAS
