from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester, BGPSimpleAS, Graph025
from bgp_simulator_pkg import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubprefixGraph025Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph025
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (4, 10, enums.ASNs.VICTIM.value, )  # Do I need to add the victim here?


class Test088(BaseSubprefixGraph025Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test089(BaseSubprefixGraph025Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test090(BaseSubprefixGraph025Tester):
    AdoptASCls = ROVPPV2aSimpleAS

