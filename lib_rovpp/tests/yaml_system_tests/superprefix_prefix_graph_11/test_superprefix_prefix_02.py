from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, ROVSimpleAS, Graph011

from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....as_classes import ROVPPV3AS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix02Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph011
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (5, 6, 1, 11, 12)


class Test024SupreprefixPrefix02(BaseSuperPrefixPrefix02Tester):
    AdoptASCls = ROVSimpleAS

class Test025SupreprefixPrefix02(BaseSuperPrefixPrefix02Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test026SupreprefixPrefix02(BaseSuperPrefixPrefix02Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test027SupreprefixPrefix02(BaseSuperPrefixPrefix02Tester):
    AdoptASCls = ROVPPV2aSimpleAS

