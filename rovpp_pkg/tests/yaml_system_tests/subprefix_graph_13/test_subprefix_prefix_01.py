from pathlib import Path

from lib_bgp_simulator import BaseGraphSystemTester
from lib_bgp_simulator import BGPSimpleAS
from lib_bgp_simulator import ROVSimpleAS
from lib_bgp_simulator import Graph013

from ..unstable import Unstable
from ....as_classes import ROVPPV1SimpleAS
from ....as_classes import ROVPPV2SimpleAS
from ....as_classes import ROVPPV2aSimpleAS

from ....engine_input import ROVPPSubprefixHijack


class BaseSubPrefix01Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph013
    BaseASCls = BGPSimpleAS
    EngineInputCls = ROVPPSubprefixHijack
    base_dir = Path(__file__).parent
    adopting_asns = (2, )


class Test021SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVSimpleAS


class Test022SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV1SimpleAS


class Test023SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV2SimpleAS


class Test024SubprefixPrefix01(BaseSubPrefix01Tester):
    AdoptASCls = ROVPPV2aSimpleAS
