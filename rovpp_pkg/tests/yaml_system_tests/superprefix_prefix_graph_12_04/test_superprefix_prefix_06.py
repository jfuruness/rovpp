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


class BaseSuperPrefixPrefix06Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph012
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (2, 4, 11)


class Test053SupreprefixPrefix06(BaseSuperPrefixPrefix06Tester):
    AdoptASCls = ROVSimpleAS


class Test054SupreprefixPrefix06(BaseSuperPrefixPrefix06Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test055SupreprefixPrefix06(BaseSuperPrefixPrefix06Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test056SupreprefixPrefix06(BaseSuperPrefixPrefix06Tester):
    AdoptASCls = ROVPPV2aSimpleAS
