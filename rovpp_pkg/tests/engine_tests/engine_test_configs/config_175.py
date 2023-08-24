from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_037
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPAnn
from bgpy import ROVSimpleAS

config_175 = EngineTestConfig(
    name="175",
    desc="Subprefix Hijack Attack with ROV",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({1: ROVSimpleAS, 11: ROVSimpleAS, 12: ROVSimpleAS, 5: ROVSimpleAS, 6: ROVSimpleAS, ASNs.VICTIM.value: ROVSimpleAS})
    ),
    graph=graph_037,
    propagation_rounds=1
)
