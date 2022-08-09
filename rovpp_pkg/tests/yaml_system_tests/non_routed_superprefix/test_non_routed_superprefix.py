from pathlib import Path

from bgp_simulator_pkg import BaseNonRoutedSuperprefixTester
from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import Graph006

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS
from ....engine_input import ROVPPNonRoutedSuperprefixHijack


class BaseROVPPNonRoutedSuperprefixTester(Unstable,
                                          BaseNonRoutedSuperprefixTester):
    GraphInfoCls = Graph006
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPNonRoutedSuperprefixHijack
    base_dir = Path(__file__).parent


class Test014NonRoutedSuperprefixV1(BaseROVPPNonRoutedSuperprefixTester):
    AdoptASCls = ROVPPV1SimpleAS


class Test015NonRoutedSuperprefixV2(BaseROVPPNonRoutedSuperprefixTester):
    AdoptASCls = ROVPPV2SimpleAS


class Test016NonRoutedSuperprefixV2a(BaseROVPPNonRoutedSuperprefixTester):
    AdoptASCls = ROVPPV2aSimpleAS
