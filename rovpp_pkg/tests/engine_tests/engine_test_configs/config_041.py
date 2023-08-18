from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ROVSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPV2SimpleAS
from rovpp_pkg import ROVPPAnn


class Config041(EngineTestConfig):
    """Contains config options to run a test"""

    name = "041"
    desc = (
        "Subprefix Hijack from fig 3a in paper with ROV++ v2"
        " adopting at AS 4 and 8, and ROV at 7. ASes 4, 8, and 7 "
        "should be disconnected"
    )
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2SimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph004()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        4: ROVPPV2SimpleAS,
        7: ROVSimpleAS,
        8: ROVPPV2SimpleAS,
    }
    propagation_rounds = 1
