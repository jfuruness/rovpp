from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, ROVSimpleAS, Graph010

from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....as_classes import ROVPPV3AS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix01Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph010
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (2, )  # Do I need to add the victim here?


class Test020SupreprefixPrefix01(BaseSuperPrefixPrefix01Tester):
    AdoptASCls = ROVSimpleAS

class Test021SupreprefixPrefix01(BaseSuperPrefixPrefix01Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test022SupreprefixPrefix01(BaseSuperPrefixPrefix01Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test023SupreprefixPrefix01(BaseSuperPrefixPrefix01Tester):
    AdoptASCls = ROVPPV2aSimpleAS

class Test024SupreprefixPrefix01(BaseSuperPrefixPrefix01Tester):
    AdoptASCls = ROVPPV3AS

