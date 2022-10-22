from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPAnn


class Config175(EngineTestConfig):
    """Contains config options to run a test"""

    name = "175"
    desc = "Subprefix Hijack Attack with ROV"
    scenario = SubprefixHijack(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               AdoptASCls=ROVSimpleAS,
                               BaseASCls=BGPSimpleAS,
                               AnnCls=ROVPPAnn)
    graph = graphs.Graph037()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        1: ROVSimpleAS,
        11: ROVSimpleAS,
        12: ROVSimpleAS,
        5: ROVSimpleAS,
        6: ROVSimpleAS,
        ASNs.VICTIM.value: ROVSimpleAS
    }
    propagation_rounds = 1
