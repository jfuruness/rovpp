from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ROVSimpleAS
from bgpy import ASNs
from bgpy import NonRoutedSuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn


class Config099(EngineTestConfig):
    """Contains config options to run a test"""

    name = "099"
    desc = "Superprefix+prefix Attack on NonRouted Prefix with ROV"
    scenario = NonRoutedSuperprefixPrefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph006()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {2: ROVSimpleAS}
    propagation_rounds = 1
