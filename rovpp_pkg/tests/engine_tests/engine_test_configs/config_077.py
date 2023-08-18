from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import NonRoutedPrefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2SimpleAS


class Config077(EngineTestConfig):
    """Contains config options to run a test"""

    name = "077"
    desc = "NonRouted Prefix Hijack with v2"

    scenario = NonRoutedPrefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2SimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph048()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        3: ROVPPV2SimpleAS,
        4: ROVPPV2SimpleAS,
        6: ROVPPV2SimpleAS,
    }
    propagation_rounds = 1
