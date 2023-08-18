from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPV2SimpleAS
from rovpp_pkg import ROVPPAnn


class Config044(EngineTestConfig):
    """Contains config options to run a test"""

    name = "044"
    desc = "Subprefix Hijack from fig 4 in paper with ROV++ v2"
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2SimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph005()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {5: ROVPPV2SimpleAS}
    propagation_rounds = 1
