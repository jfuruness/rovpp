from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import NonRoutedPrefixHijack

from rovpp_pkg import ROVPPAnn


class Config050(EngineTestConfig):
    """Contains config options to run a test"""

    name = "050"
    desc = "Prefix hijack on a non-routed prefix. Here adopting AS 2 is " \
           "adopting ROV, and should be able to detect the attack and " \
           "drop the hijack ann, hence disconnecting itself and customer."
    scenario = NonRoutedPrefixHijack(attacker_asns={ASNs.ATTACKER.value},
                                     victim_asns={ASNs.VICTIM.value},
                                     AdoptASCls=ROVSimpleAS,
                                     BaseASCls=BGPSimpleAS,
                                     AnnCls=ROVPPAnn)
    graph = graphs.Graph006()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {2: ROVSimpleAS}
    propagation_rounds = 1
