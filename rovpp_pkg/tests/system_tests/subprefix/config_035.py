from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig
from bgp_simulator_pkg import BGPSimpleAS, ROVSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack


class Config035(EngineTestConfig):
    """Contains config options to run a test"""

    name = "035"
    desc = "Subprefix Hijack from fig 2 in paper with ROV adopting."
    scenario = SubprefixHijack(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               AdoptASCls=ROVSimpleAS,
                               BaseASCls=BGPSimpleAS)
    graph = graphs.Graph003()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {3: ROVSimpleAS,
                                                    4: ROVSimpleAS}
    propagation_rounds = 1
