from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester
from lib_bgp_simulator import BGPSimpleAS
from lib_bgp_simulator import ROVSimpleAS
from lib_bgp_simulator import Graph013

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix08Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph013
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (2, )


class Test061SupreprefixPrefix08(BaseSuperPrefixPrefix08Tester):
    AdoptASCls = ROVSimpleAS


class Test062SupreprefixPrefix08(BaseSuperPrefixPrefix08Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test063SupreprefixPrefix08(BaseSuperPrefixPrefix08Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test064SupreprefixPrefix08(BaseSuperPrefixPrefix08Tester):
    AdoptASCls = ROVPPV2aSimpleAS
