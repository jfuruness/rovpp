from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, ROVSimpleAS, Graph012

from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....as_classes import ROVPPV3AS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix06Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph012
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (2, 4, 11)


class Test040SupreprefixPrefix06(BaseSuperPrefixPrefix06Tester):
    AdoptASCls = ROVSimpleAS

class Test041SupreprefixPrefix06(BaseSuperPrefixPrefix06Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test042SupreprefixPrefix06(BaseSuperPrefixPrefix06Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test043SupreprefixPrefix06(BaseSuperPrefixPrefix06Tester):
    AdoptASCls = ROVPPV2aSimpleAS

