from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, Graph033
from lib_bgp_simulator import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubprefixGraph033Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph033
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (3, 4, 6, enums.ASNs.VICTIM.value, )  # Do I need to add the victim here?


class Test108(BaseSubprefixGraph033Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test109(BaseSubprefixGraph033Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test110(BaseSubprefixGraph033Tester):
    AdoptASCls = ROVPPV2aSimpleAS

