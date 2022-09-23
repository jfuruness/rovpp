from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import NonRoutedPrefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV1SimpleAS

class Config088(EngineTestConfig):
    """Contains config options to run a test"""

    name = "088"
    desc = "NonRouted Prefix Hijack with v1"

    scenario = NonRoutedPrefixHijack(attacker_asns={ASNs.ATTACKER.value},
                                     victim_asns={ASNs.VICTIM.value},
                                     AdoptASCls=ROVPPV1SimpleAS,
                                     BaseASCls=BGPSimpleAS,
                                     AnnCls=ROVPPAnn)
    graph = graphs.Graph051()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {4: ROVPPV1SimpleAS}
    propagation_rounds = 1
