from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ROVSimpleAS
from bgpy import ASNs
from bgpy import SuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn


class Config060(EngineTestConfig):
    """Contains config options to run a test"""

    name = "060"
    desc = (
        "This is running as single adopting AS (ROV AS 12).\n"
        "This is 22 AS topology "
        "with a clique at the top with 1,2,3, and 4.\nIts about 4 levels "
        "tall.\nThe attacker under the same provider as the legitmated "
        "origin\n(i.e. they’re both on the edge next to each other)."
    )

    scenario = SuperprefixPrefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph016()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {12: ROVSimpleAS}
    propagation_rounds = 1
