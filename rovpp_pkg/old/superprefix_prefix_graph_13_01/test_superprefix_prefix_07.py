from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester
from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import Graph013

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix07Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph013
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (6, )


class Test057SupreprefixPrefix07(BaseSuperPrefixPrefix07Tester):
    AdoptASCls = ROVSimpleAS


class Test058SupreprefixPrefix07(BaseSuperPrefixPrefix07Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test059SupreprefixPrefix07(BaseSuperPrefixPrefix07Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test060SupreprefixPrefix07(BaseSuperPrefixPrefix07Tester):
    AdoptASCls = ROVPPV2aSimpleAS
