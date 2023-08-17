from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2SimpleAS


class Config177(EngineTestConfig):
    """Contains config options to run a test"""

    name = "177"
    desc = "Subprefix Hijack Attack with v2"
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2SimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph037()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        1: ROVPPV2SimpleAS,
        11: ROVPPV2SimpleAS,
        12: ROVPPV2SimpleAS,
        5: ROVPPV2SimpleAS,
        6: ROVPPV2SimpleAS,
        ASNs.VICTIM.value: ROVPPV2SimpleAS,
    }
    propagation_rounds = 1
