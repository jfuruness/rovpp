from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPV2LiteSimpleAS
from rovpp_pkg import ROVPPAnn


class Config046(EngineTestConfig):
    """Contains config options to run a test"""

    name = "046"
    desc = (
        "Subprefix Hijack that tests blackhole announcements are not sent"
        "if hijack comes from customers with ROV++ v2 lite"
    )
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2LiteSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph008()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {1: ROVPPV2LiteSimpleAS}
    propagation_rounds = 1
