from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPV3AS
from rovpp_pkg import ROVPPAnn


class Config045(EngineTestConfig):
    """Contains config options to run a test"""

    name = "045"
    desc = "Subprefix Hijack to test ROV++ v3."
    scenario = SubprefixHijack(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               AdoptASCls=ROVPPV3AS,
                               BaseASCls=BGPSimpleAS,
                               AnnCls=ROVPPAnn)
    graph = graphs.Graph005()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {5: ROVPPV3AS,
                                                    8: ROVPPV3AS,
                                                    10: ROVPPV3AS,
                                                    15: ROVPPV3AS}
    propagation_rounds = 1
