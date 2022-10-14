from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPV2aLiteSimpleAS
from rovpp_pkg import ROVPPAnn


class Config048(EngineTestConfig):
    """Contains config options to run a test"""

    name = "048"
    desc = ("Subprefix Hijack that tests blackhole announcements\nshould "
            "be sent, even if hijack comes from a customer\nwith ROV++ v2a "
            "lite.\nThis comes with the added check to see if it gets "
            "sent to peers.")
    scenario = SubprefixHijack(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               AdoptASCls=ROVPPV2aLiteSimpleAS,
                               BaseASCls=BGPSimpleAS,
                               AnnCls=ROVPPAnn)
    graph = graphs.Graph008()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {1: ROVPPV2aLiteSimpleAS}
    propagation_rounds = 1
