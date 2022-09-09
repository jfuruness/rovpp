from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2SimpleAS


class Config071(EngineTestConfig):
    """Contains config options to run a test"""

    name = "071"
    desc = "ROV++ v2 adopting" \
           "Example where v1 leads a higher disconnection rate and " \
           "lower successful connection rate than v2 (for non-adopting " \
           "ASes). AS 57 is the legit origin (of 1.2/16), 666 " \
           "does subprefix as usual. AS 33 and AS 1 are adopters " \
           "(of ROV++ , v1 or v2 " \
           "as desired). If 33 and 1 adopt v1, then 33 blackholes 1.2.3/24 " \
           "and announces 1.2/16 to 1, with AS path of 33-34-57. So AS 1 " \
           "prefers this (shorter) path, cf to the " \
           "alternative: 11-12-135-57. This causes disconnection by the " \
           "blackhole that was set up at 33. " \
           "If 33 and 1 adopt v2, then AS 1 will receive the blackhole " \
           "announcement from 33 and hence prefer the hole-free route via 11 " \
           "(which only has announcement 1.2/16), and hence route " \
           "the traffic correctly to the origin. If AS 33 and AS 1 " \
           "use v1 Lite, then " \
           "AS 1 will still use the path via AS 33, and hence will " \
           "have the same results as those when the policy is v1."

    scenario = SubprefixHijack(attacker_asns={ASNs.ATTACKER.value},
                               victim_asns={ASNs.VICTIM.value},
                               AdoptASCls=ROVPPV2SimpleAS,
                               BaseASCls=BGPSimpleAS,
                               AnnCls=ROVPPAnn)
    graph = graphs.Graph038()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {1: ROVPPV2SimpleAS,
                                                    33: ROVPPV2SimpleAS}
    propagation_rounds = 1
