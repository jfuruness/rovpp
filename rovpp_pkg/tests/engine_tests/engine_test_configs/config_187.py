from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_014
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS, ROVSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPAnn


config_187 = EngineTestConfig(
    name="187",
    desc="Subprefix Hijack Attack with ROV",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({6: ROVSimpleAS})
    ),
    graph=graph_014,
    propagation_rounds=1
)
