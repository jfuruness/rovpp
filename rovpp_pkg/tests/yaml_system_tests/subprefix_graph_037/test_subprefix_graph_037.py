from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester, ROVSimpleAS, BGPSimpleAS, Graph037
from bgp_simulator_pkg import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV3AS

from ....engine_input import ROVPPSubprefixHijack


class BaseUnstableSubprefixGraph037Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph037
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (1, 11, 12, 5, 6, enums.ASNs.VICTIM.value, )

class BaseSubprefixGraph037Tester(BaseGraphSystemTester):
    GraphInfoCls = Graph037
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (1, 11, 12, 5, 6, enums.ASNs.VICTIM.value, )


class Test122(BaseUnstableSubprefixGraph037Tester):
    AdoptASCls = ROVPPV1SimpleAS

class Test123(BaseUnstableSubprefixGraph037Tester):
    AdoptASCls = ROVPPV2SimpleAS

class Test124(BaseSubprefixGraph037Tester):
    AdoptASCls = ROVPPV3AS

class Test125(BaseSubprefixGraph037Tester):
    AdoptASCls = ROVSimpleAS
