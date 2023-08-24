from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_038
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPAnn, ROVPPV2SimpleAS


config_071 = EngineTestConfig(
    name="071",
    desc=(
        "ROV++ v2 adopting\n"
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
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2SimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            1: ROVPPV2SimpleAS,
            33: ROVPPV2SimpleAS,
        }),
        AnnCls=ROVPPAnn
    ),
    graph=graph_038,
)
