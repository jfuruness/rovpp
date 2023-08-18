from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import ROVSimpleAS
from bgpy import SuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn


class Config135(EngineTestConfig):
    """Contains config options to run a test"""

    name = "135"
    desc = "Superprefix+Prefix Attack on Prefix with ROV"
    scenario = SuperprefixPrefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph013()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {2: ROVSimpleAS}
    propagation_rounds = 1
