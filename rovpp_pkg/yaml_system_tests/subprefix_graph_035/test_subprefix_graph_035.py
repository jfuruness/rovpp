from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester, BGPSimpleAS, Graph035
from bgp_simulator_pkg import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2LiteSimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubprefixGraph035Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph035
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (4, enums.ASNs.VICTIM.value, )  # Do I need to add the victim here?


class Test116(BaseSubprefixGraph035Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test117(BaseSubprefixGraph035Tester):
    AdoptASCls = ROVPPV2LiteSimpleAS

class Test118(BaseSubprefixGraph035Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test119(BaseSubprefixGraph035Tester):
    AdoptASCls = ROVPPV2aLiteSimpleAS

class Test120(BaseSubprefixGraph035Tester):
    AdoptASCls = ROVPPV2aSimpleAS

