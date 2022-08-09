from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester
from lib_bgp_simulator import BGPSimpleAS
from lib_bgp_simulator import ROVSimpleAS
from lib_bgp_simulator import Graph012

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix04Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph012
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (2, 4)


class Test045SupreprefixPrefix04(BaseSuperPrefixPrefix04Tester):
    AdoptASCls = ROVSimpleAS


class Test046SupreprefixPrefix04(BaseSuperPrefixPrefix04Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test047SupreprefixPrefix04(BaseSuperPrefixPrefix04Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test048SupreprefixPrefix04(BaseSuperPrefixPrefix04Tester):
    AdoptASCls = ROVPPV2aSimpleAS
