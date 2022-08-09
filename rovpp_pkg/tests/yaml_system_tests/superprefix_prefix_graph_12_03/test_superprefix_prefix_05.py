from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester
from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import Graph012

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix05Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph012
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (10, 2, 4)


class Test049SupreprefixPrefix05(BaseSuperPrefixPrefix05Tester):
    AdoptASCls = ROVSimpleAS


class Test050SupreprefixPrefix05(BaseSuperPrefixPrefix05Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test051SupreprefixPrefix05(BaseSuperPrefixPrefix05Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test052SupreprefixPrefix05(BaseSuperPrefixPrefix05Tester):
    AdoptASCls = ROVPPV2aSimpleAS
