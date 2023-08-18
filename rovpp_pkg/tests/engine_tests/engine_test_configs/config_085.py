from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import NonRoutedSuperprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2SimpleAS


class Config085(EngineTestConfig):
    """Contains config options to run a test"""

    name = "085"
    desc = "Superprefix Attack on NonRouted Prefix with v2"

    scenario = NonRoutedSuperprefixHijack(
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
