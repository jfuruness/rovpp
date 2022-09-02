from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2SimpleAS


class Config074(EngineTestConfig):
    """Contains config options to run a test"""

    name = "074"
    desc = "ROV++ v2 adopting" \
           "Example where v2 leads to a higher disconnection " \
           "rate and lower successful connection rate (for non-adopting ASes)." \
           "When AS 33 adopts v2, it sends a blackhole announcement to " \
           "AS 3, which will be further forwarded to AS 3’s customer" \
           "cone. When AS 33 adopts v1, it only sets up a local " \
           "blackhole. AS 3 only receives one announcement (1.2/16) " \
           "from AS 1 and" \
           "no other announcement. It will hence route traffic destining " \
           "to 1.2.3/24 via AS 1 to the legit origin, AS 5. " \
           "Similarly, AS 3’s " \
           "customers’ traffic to 1.2.3/24 will be routed successfully. " \
           "In the figure, whether AS 5 adopts ROV++ or not does not matter " \
           "since the hijack announcement will not be sent out by " \
           "AS 5 to AS 1 anyway (due to valley-free routing)."

    scenario = SubprefixHijack(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               AdoptASCls=ROVPPV2SimpleAS,
                               BaseASCls=BGPSimpleAS,
                               AnnCls=ROVPPAnn)
    graph = graphs.Graph039()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {33: ROVPPV2SimpleAS}
    propagation_rounds = 1
