from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester
from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import Graph016

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubPrefix02Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph016
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (12, )


class Test029SubprefixPrefix02(BaseSubPrefix02Tester):
    AdoptASCls = ROVSimpleAS


class Test030SubprefixPrefix02(BaseSubPrefix02Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test031SubprefixPrefix02(BaseSubPrefix02Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test032SubprefixPrefix02(BaseSubPrefix02Tester):
    AdoptASCls = ROVPPV2aSimpleAS
