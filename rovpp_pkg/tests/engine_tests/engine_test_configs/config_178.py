from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2aSimpleAS


class Config178(EngineTestConfig):
    """Contains config options to run a test"""

    name = "178"
    desc = "Subprefix Hijack Attack with v2a"
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2aSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph037()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        1: ROVPPV2aSimpleAS,
        11: ROVPPV2aSimpleAS,
        12: ROVPPV2aSimpleAS,
        5: ROVPPV2aSimpleAS,
        6: ROVPPV2aSimpleAS,
        ASNs.VICTIM.value: ROVPPV2aSimpleAS,
    }
    propagation_rounds = 1
