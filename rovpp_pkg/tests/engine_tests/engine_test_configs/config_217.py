from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import NonRoutedSuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2SimpleAS


class Config217(EngineTestConfig):
    """Contains config options to run a test"""

    name = "217"
    desc = "Superprefix+Prefix Attack on NonRouted Prefix with v2"
    scenario = NonRoutedSuperprefixPrefixHijack(attacker_asns={ASNs.ATTACKER.value},
                                                victim_asns={ASNs.VICTIM.value},
                                                AdoptASCls=ROVPPV2SimpleAS,
                                                BaseASCls=BGPSimpleAS,
                                                AnnCls=ROVPPAnn)
    graph = graphs.Graph050()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {3: ROVPPV2SimpleAS,
                                                    4: ROVPPV2SimpleAS,
                                                    6: ROVPPV2SimpleAS}
    propagation_rounds = 1
