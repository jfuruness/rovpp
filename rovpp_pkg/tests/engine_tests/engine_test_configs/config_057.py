from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import NonRoutedSuperprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2aSimpleAS


class Config057(EngineTestConfig):
    """Contains config options to run a test"""

    name = "057"
    desc = "Superprefix hijack on a non-routed prefix. Here adopting AS 2 " \
           "is adopting ROV++ v2a, and should send a blackhole ann for " \
           "the non-routed prefix, but accept the superprefix. It " \
           "will disconnect itself and its customer."
    scenario = NonRoutedSuperprefixHijack(attacker_asns={ASNs.ATTACKER.value},
                                          victim_asns={ASNs.VICTIM.value},
                                          AdoptASCls=ROVPPV2aSimpleAS,
                                          BaseASCls=BGPSimpleAS,
                                          AnnCls=ROVPPAnn)
    graph = graphs.Graph006()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {2: ROVPPV2aSimpleAS}
    propagation_rounds = 1
