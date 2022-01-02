from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester
from lib_bgp_simulator import BGPSimpleAS
from lib_bgp_simulator import ROVSimpleAS
from lib_bgp_simulator import Graph010

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix01Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph010
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (2, )


class Test033SupreprefixPrefix01(BaseSuperPrefixPrefix01Tester):
    AdoptASCls = ROVSimpleAS


class Test034SupreprefixPrefix01(BaseSuperPrefixPrefix01Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test035SupreprefixPrefix01(BaseSuperPrefixPrefix01Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test036SupreprefixPrefix01(BaseSuperPrefixPrefix01Tester):
    AdoptASCls = ROVPPV2aSimpleAS
