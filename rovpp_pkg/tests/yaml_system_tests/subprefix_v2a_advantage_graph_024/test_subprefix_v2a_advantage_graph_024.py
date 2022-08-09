from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, Graph024
from lib_bgp_simulator import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubprefixGraph024Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph024
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (4, 10, enums.ASNs.VICTIM.value, )  # Do I need to add the victim here?


class Test085(BaseSubprefixGraph024Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test086(BaseSubprefixGraph024Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test087(BaseSubprefixGraph024Tester):
    AdoptASCls = ROVPPV2aSimpleAS

