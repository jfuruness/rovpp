from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester, BGPSimpleAS, Graph039
from bgp_simulator_pkg import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubprefixGraph039Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph039
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (enums.ASNs.VICTIM.value, 33)


class Test128(BaseSubprefixGraph039Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test129(BaseSubprefixGraph039Tester):
    AdoptASCls = ROVPPV2SimpleAS

