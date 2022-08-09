from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, Graph034
from lib_bgp_simulator import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2LiteSimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubprefixGraph034Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph034
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (3, 4, 6, enums.ASNs.VICTIM.value, )  # Do I need to add the victim here?


class Test111(BaseSubprefixGraph034Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test112(BaseSubprefixGraph034Tester):
    AdoptASCls = ROVPPV2LiteSimpleAS

class Test113(BaseSubprefixGraph034Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test114(BaseSubprefixGraph034Tester):
    AdoptASCls = ROVPPV2aLiteSimpleAS

class Test115(BaseSubprefixGraph034Tester):
    AdoptASCls = ROVPPV2aSimpleAS

