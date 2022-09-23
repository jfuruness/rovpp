from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import NonRoutedPrefixHijack
from bgp_simulator_pkg import ROVSimpleAS

from rovpp_pkg import ROVPPAnn


class Config087(EngineTestConfig):
    """Contains config options to run a test"""

    name = "087"
    desc = "NonRouted Prefix Hijack with ROV"

    scenario = NonRoutedPrefixHijack(attacker_asns={ASNs.ATTACKER.value},
                                     victim_asns={ASNs.VICTIM.value},
                                     AdoptASCls=ROVSimpleAS,
                                     BaseASCls=BGPSimpleAS,
                                     AnnCls=ROVPPAnn)
    graph = graphs.Graph051()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {4: ROVSimpleAS}
    propagation_rounds = 1
