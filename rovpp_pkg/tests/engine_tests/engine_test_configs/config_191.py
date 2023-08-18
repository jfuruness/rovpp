from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import ROVSimpleAS
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPAnn


class Config191(EngineTestConfig):
    """Contains config options to run a test"""

    name = "191"
    desc = "Subprefix Hijack Attack with ROV"
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph016()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {12: ROVSimpleAS}
    propagation_rounds = 1
