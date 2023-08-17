from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV1LiteSimpleAS


class Config072(EngineTestConfig):
    """Contains config options to run a test"""

    name = "072"
    desc = (
        "ROV++ v1 lite adopting\n"
        "Example where v2 leads to a higher disconnection "
        "rate\nand lower successful connection rate\n"
        "(for nonadopting ASes)."
        "When AS 33 adopts v2,\nit sends a blackhole announcement to "
        "AS 3,\nwhich will be further forwarded to AS 3’s customer"
        "cone.\nWhen AS 33 adopts v1,\nit only sets up a local "
        "blackhole.\nAS 3 only receives one announcement (1.2/16) "
        "from AS 1\nand"
        "no other announcement.\nIt will hence route traffic destining "
        "to 1.2.3/24 via AS 1 to the legit origin, AS 5.\n"
        "Similarly, AS 3’s "
        "customers’ traffic to 1.2.3/24 will be routed successfully.\n"
        "In the figure,\nwhether AS 5 adopts ROV++ or not doesn't matter\n"
        "since the hijack announcement will not be sent out by "
        "AS 5 to AS 1 anyway\n(due to valley-free routing)."
    )

    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV1LiteSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph039()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {33: ROVPPV1LiteSimpleAS}
    propagation_rounds = 1
