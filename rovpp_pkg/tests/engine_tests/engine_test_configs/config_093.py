from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import NonRoutedSuperprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2SimpleAS

class Config093(EngineTestConfig):
    """Contains config options to run a test"""

    name = "093"
    desc = "Superprefix Attack on NonRouted Prefix with v2"

    scenario = NonRoutedSuperprefixHijack(attacker_asns={ASNs.ATTACKER.value},
                                          victim_asns={ASNs.VICTIM.value},
                                          AdoptASCls=ROVPPV2SimpleAS,
                                          BaseASCls=BGPSimpleAS,
                                          AnnCls=ROVPPAnn)
    graph = graphs.Graph049()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {4: ROVPPV2SimpleAS}
    propagation_rounds = 1
