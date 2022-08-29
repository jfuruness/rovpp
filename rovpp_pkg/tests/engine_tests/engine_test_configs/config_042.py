from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPV2aLiteSimpleAS
from rovpp_pkg import ROVPPAnn


class Config042(EngineTestConfig):
    """Contains config options to run a test"""

    name = "042"
    desc = "Subprefix Hijack from fig 3a in paper with ROV++ v2a lite" \
           " adopting at AS 4 and 8, and ROV at 7. ASes 4, 8, and 7 " \
           "should be disconnected"
    scenario = SubprefixHijack(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               AdoptASCls=ROVPPV2aLiteSimpleAS,
                               BaseASCls=BGPSimpleAS,
                               AnnCls=ROVPPAnn)
    graph = graphs.Graph004()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {4: ROVPPV2aLiteSimpleAS,
                                                    7: ROVSimpleAS,
                                                    8: ROVPPV2aLiteSimpleAS}
    propagation_rounds = 1
