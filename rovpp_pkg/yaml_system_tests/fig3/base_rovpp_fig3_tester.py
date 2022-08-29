from pathlib import Path

from bgp_simulator_pkg import BaseGraphSystemTester, Graph004, BGPSimpleAS

from ..unstable import Unstable
from ....engine_input import ROVPPSubprefixHijack


class BaseROVPPFig3Tester(Unstable, BaseGraphSystemTester):
    GraphInfoCls = Graph004
    EngineInputCls = ROVPPSubprefixHijack
    BaseASCls = BGPSimpleAS
    base_dir = Path(__file__).parent
