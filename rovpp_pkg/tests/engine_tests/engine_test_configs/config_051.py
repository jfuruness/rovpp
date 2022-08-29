from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import NonRoutedPrefixHijack

from rovpp_pkg import ROVPPV1SimpleAS
from rovpp_pkg import ROVPPAnn


class Config051(EngineTestConfig):
    """Contains config options to run a test"""

    name = "051"
    desc = "Prefix hijack on a non-routed prefix. Here adopting AS 2 is " \
           "adopting ROV++ v1, and should detect the " \
           "attack and create a local blackhole for itself and disconnect " \
           "its customer."
    scenario = NonRoutedPrefixHijack(attacker_asns={ASNs.ATTACKER.value},
                                     victim_asns={ASNs.VICTIM.value},
                                     AdoptASCls=ROVPPV1SimpleAS,
                                     BaseASCls=BGPSimpleAS,
                                     AnnCls=ROVPPAnn)
    graph = graphs.Graph006()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {2: ROVPPV1SimpleAS}
    propagation_rounds = 1
