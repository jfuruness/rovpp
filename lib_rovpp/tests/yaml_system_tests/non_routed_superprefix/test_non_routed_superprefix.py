from pathlib import Path

from lib_bgp_simulator import BaseNonRoutedSuperprefixTester, BGPSimpleAS, Graph006


from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....engine_input import ROVPPNonRoutedSuperprefixHijack


class BaseROVPPNonRoutedSuperprefixTester(BaseNonRoutedSuperprefixTester):
    GraphInfoCls = Graph006
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPNonRoutedSuperprefixHijack
    base_dir = Path(__file__).parent


class Test011NonRoutedSuperprefixV1(BaseROVPPNonRoutedSuperprefixTester):
    AdoptASCls = ROVPPV1SimpleAS

class Test012NonRoutedSuperprefixV2(BaseROVPPNonRoutedSuperprefixTester):
    AdoptASCls = ROVPPV2SimpleAS

class Test013NonRoutedSuperprefixV2a(BaseROVPPNonRoutedSuperprefixTester):
    AdoptASCls = ROVPPV2aSimpleAS
