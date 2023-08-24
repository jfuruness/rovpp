from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_008
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPV2SimpleAS, ROVPPAnn


config_047 = EngineTestConfig(
    name="047",
    desc=(
        "Subprefix Hijack that tests blackhole announcements aren't sent"
        " if hijack comes from customers with ROV++ v2"
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2SimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({1: ROVPPV2SimpleAS}),
        AnnCls=ROVPPAnn
    ),
    graph=graph_008,
)
