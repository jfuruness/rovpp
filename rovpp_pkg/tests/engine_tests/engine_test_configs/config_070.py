from typing import Dict, Type

from caida_collector_pkg import AS

from bgp_simulator_pkg import graphs
from bgp_simulator_pkg import EngineTestConfig

from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import ASNs
from bgp_simulator_pkg import SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV1SimpleAS


class Config070(EngineTestConfig):
    """Contains config options to run a test"""

    name = "070"
    desc = (
        "ROV++ v1 lite adopting\n"
        "Example where v1 leads a higher disconnection rate\nand "
        "lower successful connection rate\nthan v2 (for non-adopting "
        "ASes).\nAS 57 is the legit origin (of 1.2/16),\n666 "
        "does subprefix as usual.\nAS 33 and AS 1 are adopters\n"
        "(of ROV++ , v1 or v2 "
        "as desired).\nIf 33 and 1 adopt v1, then 33 blackholes 1.2.3/24 "
        "and announces 1.2/16 to 1, with AS path of 33-34-57.\nSo AS 1 "
        "prefers this (shorter) path, cf to the "
        "alternative: 11-12-135-57.\nThis causes disconnection by the "
        "blackhole that was set up at 33.\n"
        "If 33 and 1 adopt v2,\nthen AS 1 will receive the blackhole "
        "announcement from 33\nand hence prefer the hole-free route via 11"
        "\n(which only has announcement 1.2/16),\nand hence route "
        "the traffic correctly to the origin.\nIf AS 33 and AS 1 "
        "use v1 Lite,\nthen "
        "AS 1 will still use the path via AS 33,\nand hence will "
        "have the same results as those when the policy is v1."
    )

    scenario = SubprefixHijack(
        attacker_asns={ASNs.ATTACKER.value},
        victim_asns={ASNs.VICTIM.value},
        AdoptASCls=ROVPPV1SimpleAS,
        BaseASCls=BGPSimpleAS,
        AnnCls=ROVPPAnn,
    )
    graph = graphs.Graph038()
    non_default_as_cls_dict: Dict[int, Type[AS]] = {
        1: ROVPPV1SimpleAS,
        33: ROVPPV1SimpleAS,
    }
    propagation_rounds = 1
