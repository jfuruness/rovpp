from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPV2aSimpleAS
from rovpp_pkg import ROVPPAnn


class Config049(EngineTestConfig):
    """Contains config options to run a test"""

    name = "049"
    desc = (
        "Subprefix Hijack that tests blackhole announcements\nshould "
        "be sent, even if hijack comes from a customer\nwith ROV++ v2a "
        "\nThis comes with the added check to see if it gets "
        "sent to peers."
    )
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2aSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph008()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {1: ROVPPV2aSimpleAS}
    propagation_rounds = 1
