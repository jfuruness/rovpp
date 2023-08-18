from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2aSimpleAS


class Config204(EngineTestConfig):
    """Contains config options to run a test"""

    name = "204"
    desc = ""
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2aSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph027()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        4: ROVPPV2aSimpleAS,
        10: ROVPPV2aSimpleAS,
        ASNs.VICTIM.value: ROVPPV2aSimpleAS,
    }
    propagation_rounds = 1
