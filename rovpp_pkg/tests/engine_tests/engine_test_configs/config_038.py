from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ROVSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPV1LiteSimpleAS
from rovpp_pkg import ROVPPAnn


class Config038(EngineTestConfig):
    """Contains config options to run a test"""

    name = "038"
    desc = (
        "Subprefix Hijack from fig 3a in paper with ROV++ v1 adopting at "
        "AS 4, and ROV at 7 and 8."
    )
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV1LiteSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph004()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        4: ROVPPV1LiteSimpleAS,
        7: ROVSimpleAS,
        8: ROVSimpleAS,
    }
    propagation_rounds = 1
