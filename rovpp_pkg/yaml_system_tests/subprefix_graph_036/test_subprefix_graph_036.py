from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester, BGPSimpleAS, Graph036
from bgp_simulator_pkg import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV3AS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubprefixGraph036Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph036
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (5, 8, 10, 15, enums.ASNs.VICTIM.value, )  # Do I need to add the victim here?


class Test121(BaseSubprefixGraph036Tester):
    AdoptASCls = ROVPPV3AS

