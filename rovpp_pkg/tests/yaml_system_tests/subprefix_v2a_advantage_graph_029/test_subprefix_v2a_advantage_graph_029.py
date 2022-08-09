from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester, BGPSimpleAS, Graph029
from lib_bgp_simulator import enums

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aLiteSimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubprefixGraph029Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph029
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (4, 10, enums.ASNs.VICTIM.value, )  # Do I need to add the victim here?


class Test096(BaseSubprefixGraph029Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test097(BaseSubprefixGraph029Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test098(BaseSubprefixGraph029Tester):
    AdoptASCls = ROVPPV2aSimpleAS

