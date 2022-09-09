from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2LiteSimpleAS


class Config062(EngineTestConfig):
    """Contains config options to run a test"""

    name = "062"
    desc = "This is running as single adopting AS (ROV++ v2 lite AS 12). " \
           "This is 22 AS topology " \
           "with a clique at the top with 1,2,3, and 4. Its about 4 levels " \
           "tall. The attacker under the same provider as the legitmated " \
           "origin (i.e. they’re both on the edge right next to each other). " \

    scenario = SuperprefixPrefixHijack(attacker_asns={ASNs.ATTACKER.value},
                                       victim_asns={ASNs.VICTIM.value},
                                       AdoptASCls=ROVPPV2LiteSimpleAS,
                                       BaseASCls=BGPSimpleAS,
                                       AnnCls=ROVPPAnn)
    graph = graphs.Graph016()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {12: ROVPPV2LiteSimpleAS}
    propagation_rounds = 1
