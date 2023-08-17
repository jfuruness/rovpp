from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2SimpleAS


class Config058(EngineTestConfig):
    """Contains config options to run a test"""

    name = "058"
    desc = (
        "This is a v2 test.\nA suggested test for v2 versus v2a. "
        "v2a leads to additional "
        "benefits over v2.\nWhen AS 4 uses v2, AS 7 and its customer cone "
        "will be hijacked.\nWhen AS 4 uses v2a, the blackhole announcement"
        " from AS 4 will compete with the hijack announcement.\nIn this "
        "case, AS 7 will choose the blackhole announcement,\nand hence "
        "AS 7 and its customer cone\nwill be will be disconnected "
        "instead of hijacked."
    )

    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2SimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph022()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {4: ROVPPV2SimpleAS}
    propagation_rounds = 1
