from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPAS, Graph005

from ..unstable import Unstable
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV3AS
from ....engine_input import ROVPPSubprefixHijack


class BaseROVPPFig4Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph005
    BaseASCls = BGPAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = [5, 8, 10, 15]


class Test009Fig2V2(BaseROVPPFig4Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test010Fig2V3(BaseROVPPFig4Tester):
    AdoptASCls = ROVPPV3AS
