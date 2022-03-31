from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, Graph038
from lib_bgp_simulator import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubprefixGraph038Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph038
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (1, 33)


class Test126(BaseSubprefixGraph038Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test127(BaseSubprefixGraph038Tester):
    AdoptASCls = ROVPPV2SimpleAS

