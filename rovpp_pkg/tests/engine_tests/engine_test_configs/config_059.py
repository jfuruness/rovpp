from typing import Dict, Type

from caida_collector_pkg import AS

from bgpy import graphs
from bgpy import EngineTestConfig

from bgpy import BGPSimpleAS
from bgpy import ASNs
from bgpy import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2aSimpleAS


class Config059(EngineTestConfig):
    """Contains config options to run a test"""

    name = "059"
    desc = (
        "This is a v2a test.\nA suggested test for v2 versus v2a.\n"
        "v2a leads to additional "
        "benefits over v2.\nWhen AS 4 uses v2, AS 7 and its customer cone "
        "will be hijacked.\nWhen AS 4 uses v2a, the blackhole announcement"
        " from AS 4 will compete with the hijack announcement.\nIn this "
        "case, AS 7 will choose the blackhole announcement,\nand hence "
        "AS 7 and its customer cone\nwill be will be disconnected "
        "instead of hijacked."
    )

    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV2aSimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph022()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {4: ROVPPV2aSimpleAS}
    propagation_rounds = 1
