from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV1SimpleAS


class Config176(EngineTestConfig):
    """Contains config options to run a test"""

    name = "176"
    desc = "Subprefix Hijack Attack with v1"
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV1SimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph037()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        1: ROVPPV1SimpleAS,
        11: ROVPPV1SimpleAS,
        12: ROVPPV1SimpleAS,
        5: ROVPPV1SimpleAS,
        6: ROVPPV1SimpleAS,
        ASNs.VICTIM.value: ROVPPV1SimpleAS,
    }
    propagation_rounds = 1
