from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2SimpleAS


class Config173(EngineTestConfig):
    """Contains config options to run a test"""

    name = "173"
    desc = "Subprefix Hijack Attack with v2"
    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2SimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph036()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        5: ROVPPV2SimpleAS,
        8: ROVPPV2SimpleAS,
        10: ROVPPV2SimpleAS,
        15: ROVPPV2SimpleAS,
        ASNs.VICTIM.value: ROVPPV2SimpleAS,
    }
    propagation_rounds = 1
