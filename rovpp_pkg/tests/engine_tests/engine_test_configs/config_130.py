from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2aSimpleAS


class Config130(EngineTestConfig):
    """Contains config options to run a test"""

    name = "130"
    desc = "Superprefix+Prefix Attack on Prefix with v2a"
    scenario = SuperprefixPrefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2aSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph012()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        2: ROVPPV2aSimpleAS,
        4: ROVPPV2aSimpleAS,
        11: ROVPPV2aSimpleAS,
    }
    propagation_rounds = 1
