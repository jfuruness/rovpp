from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester
from lib_bgp_simulator import BGPSimpleAS
from lib_bgp_simulator import ROVSimpleAS
from lib_bgp_simulator import Graph016

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix09Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph016
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (12, )


class Test065SupreprefixPrefix09(BaseSuperPrefixPrefix09Tester):
    AdoptASCls = ROVSimpleAS


class Test066SupreprefixPrefix09(BaseSuperPrefixPrefix09Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test067SupreprefixPrefix09(BaseSuperPrefixPrefix09Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test068SupreprefixPrefix09(BaseSuperPrefixPrefix09Tester):
    AdoptASCls = ROVPPV2aSimpleAS
