from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, ROVSimpleAS, Graph012

from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....as_classes import ROVPPV3AS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix03Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph012
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (1, 2, 3, 8, 9)


class Test028SupreprefixPrefix03(BaseSuperPrefixPrefix03Tester):
    AdoptASCls = ROVSimpleAS

class Test029SupreprefixPrefix03(BaseSuperPrefixPrefix03Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test030SupreprefixPrefix03(BaseSuperPrefixPrefix03Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test031SupreprefixPrefix03(BaseSuperPrefixPrefix03Tester):
    AdoptASCls = ROVPPV2aSimpleAS

