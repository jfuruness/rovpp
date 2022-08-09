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


class BaseSuperPrefixPrefix03Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph012
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (1, 2, 3, 8, 9)


class Test041SupreprefixPrefix03(BaseSuperPrefixPrefix03Tester):
    AdoptASCls = ROVSimpleAS


class Test042SupreprefixPrefix03(BaseSuperPrefixPrefix03Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test043SupreprefixPrefix03(BaseSuperPrefixPrefix03Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test044SupreprefixPrefix03(BaseSuperPrefixPrefix03Tester):
    AdoptASCls = ROVPPV2aSimpleAS
