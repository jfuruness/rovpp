from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, ROVSimpleAS, Graph013

from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....as_classes import ROVPPV3AS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix07Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph013
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (6, )


class Test044SupreprefixPrefix07(BaseSuperPrefixPrefix07Tester):
    AdoptASCls = ROVSimpleAS

class Test045SupreprefixPrefix07(BaseSuperPrefixPrefix07Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test046SupreprefixPrefix07(BaseSuperPrefixPrefix07Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test047SupreprefixPrefix07(BaseSuperPrefixPrefix07Tester):
    AdoptASCls = ROVPPV2aSimpleAS

