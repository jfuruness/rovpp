from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPV1LiteSimpleAS
from rovpp_pkg import ROVPPAnn

class Config036(EngineTestConfig):
    """Contains config options to run a test"""

    name = "036"
    desc = "Subprefix Hijack from fig 2 in paper with ROV++ v1 adopting."
    scenario = SubprefixHijack(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               AdoptASCls=ROVPPV1LiteSimpleAS,
                               BaseASCls=BGPSimpleAS,
                               AnnCls=ROVPPAnn)
    graph = graphs.Graph003()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {3: ROVPPV1LiteSimpleAS,
                                                    4: ROVPPV1LiteSimpleAS}
    propagation_rounds = 1
