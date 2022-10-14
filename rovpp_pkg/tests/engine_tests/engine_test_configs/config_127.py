from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import SuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn


class Config127(EngineTestConfig):
    """Contains config options to run a test"""

    name = "127"
    desc = "Superprefix+Prefix Attack on Prefix with ROV"
    scenario = SuperprefixPrefixHijack(attacker_asns={ASNs.ATTACKER.value},
                                       victim_asns={ASNs.VICTIM.value},
                                       AdoptASCls=ROVSimpleAS,
                                       BaseASCls=BGPSimpleAS,
                                       AnnCls=ROVPPAnn)
    graph = graphs.Graph012()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {2: ROVSimpleAS,
                                                    4: ROVSimpleAS,
                                                    11: ROVSimpleAS}
    propagation_rounds = 1
