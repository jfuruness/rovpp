from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import NonRoutedSuperprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV1SimpleAS


class Config055(EngineTestConfig):
    """Contains config options to run a test"""

    name = "055"
    desc = "Superprefix hijack on a non-routed prefix with v1"
    scenario = NonRoutedSuperprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV1SimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph006()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {2: ROVPPV1SimpleAS}
    propagation_rounds = 1
