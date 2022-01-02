from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester
from lib_bgp_simulator import BGPSimpleAS
from lib_bgp_simulator import ROVSimpleAS
from lib_bgp_simulator import Graph011

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSuperprefixPrefixHijack


class BaseSuperPrefixPrefix02Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph011
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSuperprefixPrefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (5, 6, 1, 11, 12)


class Test037SupreprefixPrefix02(BaseSuperPrefixPrefix02Tester):
    AdoptASCls = ROVSimpleAS


class Test038SupreprefixPrefix02(BaseSuperPrefixPrefix02Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test039SupreprefixPrefix02(BaseSuperPrefixPrefix02Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test040SupreprefixPrefix02(BaseSuperPrefixPrefix02Tester):
    AdoptASCls = ROVPPV2aSimpleAS
