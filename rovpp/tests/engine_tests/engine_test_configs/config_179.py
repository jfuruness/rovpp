from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_011
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS, ROVSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp import ROVPPAnn


config_179 = EngineTestConfig(
    name="179",
    desc="Subprefix Hijack Attack with ROV",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                5: ROVSimpleAS,
                6: ROVSimpleAS,
                1: ROVSimpleAS,
                11: ROVSimpleAS,
                12: ROVSimpleAS,
            }
        ),
    ),
    graph=graph_011,
    propagation_rounds=1,
)
