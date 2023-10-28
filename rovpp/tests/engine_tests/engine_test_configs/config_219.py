from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_018
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedPrefixHijack

from rovpp import ROVPPAnn, ROVPPV2JournalSimpleAS

config_219 = EngineTestConfig(
    name="219",
    desc="Non routed prefix attack with v2_journal",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2JournalSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({3}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: ROVPPV2JournalSimpleAS,
            }
        ),
    ),
    graph=graph_018,
    propagation_rounds=1,
)
