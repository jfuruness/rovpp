from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_048
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedPrefixHijack

from rovpp import ROVPPAnn
from bgpy.simulation_engine import ROVSimpleAS


config_075 = EngineTestConfig(
    name="075",
    desc="NonRouted Prefix Hijack with ROV",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVSimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                3: ROVSimpleAS,
                4: ROVSimpleAS,
                6: ROVSimpleAS,
            }
        ),
        AnnCls=ROVPPAnn,
    ),
    graph=graph_048,
)
