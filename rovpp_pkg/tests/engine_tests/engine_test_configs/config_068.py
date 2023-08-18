from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import SuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2aSimpleAS


class Config068(EngineTestConfig):
    """Contains config options to run a test"""

    name = "068"
    desc = "ROV++ v2a adopting AS 2. It is not useful in this type of attack"

    scenario = SuperprefixPrefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2aSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph010()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {2: ROVPPV2aSimpleAS}
    propagation_rounds = 1
