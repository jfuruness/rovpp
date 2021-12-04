from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, ROVSimpleAS, Graph016

from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix09Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph016
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (12, )


class Test052SupreprefixPrefix09(BaseSuperPrefixPrefix09Tester):
    AdoptASCls = ROVSimpleAS

class Test053SupreprefixPrefix09(BaseSuperPrefixPrefix09Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test054SupreprefixPrefix09(BaseSuperPrefixPrefix09Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test055SupreprefixPrefix09(BaseSuperPrefixPrefix09Tester):
    AdoptASCls = ROVPPV2aSimpleAS

