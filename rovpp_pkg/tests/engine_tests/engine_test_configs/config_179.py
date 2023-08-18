from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import ROVSimpleAS
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPAnn


class Config179(EngineTestConfig):
    """Contains config options to run a test"""

    name = "179"
    desc = "Subprefix Hijack Attack with ROV"
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph011()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        5: ROVSimpleAS,
        6: ROVSimpleAS,
        1: ROVSimpleAS,
        11: ROVSimpleAS,
        12: ROVSimpleAS,
    }
    propagation_rounds = 1
