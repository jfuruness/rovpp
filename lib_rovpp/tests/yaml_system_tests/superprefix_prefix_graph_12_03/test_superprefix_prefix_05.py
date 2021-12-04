from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, ROVSimpleAS, Graph012

from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....as_classes import ROVPPV3AS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix05Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph012
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (10, 2, 4)


class Test036SupreprefixPrefix05(BaseSuperPrefixPrefix05Tester):
    AdoptASCls = ROVSimpleAS

class Test037SupreprefixPrefix05(BaseSuperPrefixPrefix05Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test038SupreprefixPrefix05(BaseSuperPrefixPrefix05Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test039SupreprefixPrefix05(BaseSuperPrefixPrefix05Tester):
    AdoptASCls = ROVPPV2aSimpleAS

