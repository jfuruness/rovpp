from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_003
from bgpy.tests.engine_tests.utils import EngineTestConfig
from bgpy.simulation_engine import BGPSimpleAS, ROVSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

config_035 = EngineTestConfig(
    name="035",
    desc="Subprefix Hijack from fig 2 in paper with ROV adopting.",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVSimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({3: ROVSimpleAS, 4: ROVSimpleAS})
    ),
    graph=graph_003,
)
