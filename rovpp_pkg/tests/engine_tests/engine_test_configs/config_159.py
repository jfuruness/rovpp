from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ROVSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPAnn


class Config159(EngineTestConfig):
    """Contains config options to run a test"""

    name = "159"
    desc = ""
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph033()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        3: ROVSimpleAS,
        4: ROVSimpleAS,
        6: ROVSimpleAS,
        ASNs.VICTIM.value: ROVSimpleAS,
    }
    propagation_rounds = 1
