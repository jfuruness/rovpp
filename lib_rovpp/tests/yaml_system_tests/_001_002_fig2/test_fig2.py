from pathlib import Path

from lib_bgp_simulator import BaseFig2Tester, BGPSimpleAS

from ....as_classes import ROVPPV1LiteSimpleAS
from ....as_classes import ROVPPV1SimpleAS
from ....engine_input import ROVPPSubprefixHijack


class BaseROVPPFig2Tester(BaseFig2Tester):
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent


class Test002Fig2V1Lite(BaseROVPPFig2Tester):
    AdoptASCls = ROVPPV1LiteSimpleAS


class Test002Fig2V1(BaseROVPPFig2Tester):
    AdoptASCls = ROVPPV1SimpleAS
