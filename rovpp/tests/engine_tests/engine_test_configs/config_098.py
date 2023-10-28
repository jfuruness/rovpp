from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_051
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedSuperprefixHijack

from rovpp import ROVPPAnn, ROVPPV2aSimpleAS


config_098 = EngineTestConfig(
    name="098",
    desc="Superprefix Attack on NonRouted Prefix with v2a",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedSuperprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2aSimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({4: ROVPPV2aSimpleAS}),
        AnnCls=ROVPPAnn,
    ),
    graph=graph_051,
)
