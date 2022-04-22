from pathlib import Path

from lib_bgp_simulator import BaseNonRoutedPrefixTester, BGPSimpleAS, ROVSimpleAS, Graph006

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....engine_input import ROVPPNonRoutedPrefixHijack


class BaseROVPPNonRoutedPrefixTester(Unstable, BaseNonRoutedPrefixTester):
    GraphInfoCls = Graph006
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPNonRoutedPrefixHijack
    base_dir = Path(__file__).parent


class Test011NonRoutedPrefixV1(BaseROVPPNonRoutedPrefixTester):
    AdoptASCls = ROVSimpleAS


class Test012NonRoutedPrefixV1(BaseROVPPNonRoutedPrefixTester):
    AdoptASCls = ROVPPV1SimpleAS


class Test013NonRoutedPrefixV2(BaseROVPPNonRoutedPrefixTester):
    AdoptASCls = ROVPPV2SimpleAS


class Test014NonRoutedPrefixV2a(BaseROVPPNonRoutedPrefixTester):
    AdoptASCls = ROVPPV2aSimpleAS
