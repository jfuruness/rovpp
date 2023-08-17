from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2aSimpleAS


class Config174(EngineTestConfig):
    """Contains config options to run a test"""

    name = "174"
    desc = "Subprefix Hijack Attack with v2a"
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2aSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph036()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        5: ROVPPV2aSimpleAS,
        8: ROVPPV2aSimpleAS,
        10: ROVPPV2aSimpleAS,
        15: ROVPPV2aSimpleAS,
        ASNs.VICTIM.value: ROVPPV2aSimpleAS,
    }
    propagation_rounds = 1
