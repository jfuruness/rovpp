from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_005
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPV3AS, ROVPPAnn


config_045 = EngineTestConfig(
    name="045",
    desc="Subprefix Hijack to test ROV++ v3.",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV3AS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            5: ROVPPV3AS,
            8: ROVPPV3AS,
            10: ROVPPV3AS,
            15: ROVPPV3AS,
            18: ROVPPV3AS,
        }),
        AnnCls=ROVPPAnn
    ),
    graph=graph_005,
)
