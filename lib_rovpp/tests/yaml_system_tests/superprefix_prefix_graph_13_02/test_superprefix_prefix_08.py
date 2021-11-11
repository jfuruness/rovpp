from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, ROVSimpleAS, Graph013

from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....as_classes import ROVPPV3AS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix08Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph013
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (2, )


class Test048SupreprefixPrefix08(BaseSuperPrefixPrefix08Tester):
    AdoptASCls = ROVSimpleAS

class Test049SupreprefixPrefix08(BaseSuperPrefixPrefix08Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test050SupreprefixPrefix08(BaseSuperPrefixPrefix08Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test051SupreprefixPrefix08(BaseSuperPrefixPrefix08Tester):
    AdoptASCls = ROVPPV2aSimpleAS

