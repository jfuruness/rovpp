from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPV2SimpleAS
from rovpp_pkg import ROVPPAnn


class Config047(EngineTestConfig):
    """Contains config options to run a test"""

    name = "047"
    desc = (
        "Subprefix Hijack that tests blackhole announcements aren't sent\n"
        "if hijack comes from customers with ROV++ v2"
    )
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2SimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph008()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {1: ROVPPV2SimpleAS}
    propagation_rounds = 1
