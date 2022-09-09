from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn


class Config065(EngineTestConfig):
    """Contains config options to run a test"""

    name = "065"
    desc = "ROV adopting AS 2. It is not useful in this type of attack"

    scenario = SuperprefixPrefixHijack(attacker_asns={ASNs.ATTACKER.value},
                                       victim_asns={ASNs.VICTIM.value},
                                       AdoptASCls=ROVSimpleAS,
                                       BaseASCls=BGPSimpleAS,
                                       AnnCls=ROVPPAnn)
    graph = graphs.Graph010()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {2: ROVSimpleAS}
    propagation_rounds = 1
