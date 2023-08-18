from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import NonRoutedPrefixHijack

from rovpp_pkg import ROVPPV2aSimpleAS
from rovpp_pkg import ROVPPAnn


class Config053(EngineTestConfig):
    """Contains config options to run a test"""

    name = "053"
    desc = (
        "Prefix hijack on a non-routed prefix.\nHere adopting AS 2 is "
        "adopting ROV++ v2a,\nand should detect the "
        "attack\nand create a blackhole announcement and send it to its "
        "its customer."
    )
    scenario = NonRoutedPrefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2aSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph006()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {2: ROVPPV2aSimpleAS}
    propagation_rounds = 1
