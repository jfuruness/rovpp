from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import NonRoutedSuperprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV1SimpleAS


class Config092(EngineTestConfig):
    """Contains config options to run a test"""

    name = "092"
    desc = "Superprefix Attack on NonRouted Prefix with v1"

    scenario = NonRoutedSuperprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV1SimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph049()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {4: ROVPPV1SimpleAS}
    propagation_rounds = 1
