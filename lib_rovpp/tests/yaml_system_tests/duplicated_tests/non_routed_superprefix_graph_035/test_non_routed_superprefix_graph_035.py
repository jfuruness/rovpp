from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, Graph035
from lib_bgp_simulator import enums

from ...unstable import Unstable
from .....as_classes import ROVPPV1SimpleAS
from .....as_classes import ROVPPV2SimpleAS
from .....as_classes import ROVPPV2aSimpleAS

from .....engine_input import ROVPPNonRoutedSuperprefixHijack


class BaseSubprefixGraph035Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph035
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPNonRoutedSuperprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (4, enums.ASNs.VICTIM.value, )  # Do I need to add the victim here?


class Test116(BaseSubprefixGraph035Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test118(BaseSubprefixGraph035Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test120(BaseSubprefixGraph035Tester):
    AdoptASCls = ROVPPV2aSimpleAS

