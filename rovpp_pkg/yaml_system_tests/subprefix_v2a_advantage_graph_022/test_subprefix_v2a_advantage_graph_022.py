from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester, BGPSimpleAS, Graph022
from bgp_simulator_pkg import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubprefixGraph022Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph022
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (4, enums.ASNs.VICTIM.value, )  # Do I need to add the victim here?


class Test079(BaseSubprefixGraph022Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test080(BaseSubprefixGraph022Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test081(BaseSubprefixGraph022Tester):
    AdoptASCls = ROVPPV2aSimpleAS

