from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester, BGPSimpleAS, Graph026
from bgp_simulator_pkg import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubprefixGraph026Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph026
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (4, 10, enums.ASNs.VICTIM.value, )  # Do I need to add the victim here?


class Test091(BaseSubprefixGraph026Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test092(BaseSubprefixGraph026Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test093(BaseSubprefixGraph026Tester):
    AdoptASCls = ROVPPV2aSimpleAS

