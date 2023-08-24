from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_051
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedPrefixHijack

from rovpp_pkg import ROVPPAnn, ROVPPV1SimpleAS


config_088 = EngineTestConfig(
    name="088",
    desc="NonRouted Prefix Hijack with v1",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1SimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            4: ROVPPV1SimpleAS
        }),
        AnnCls=ROVPPAnn
    ),
    graph=graph_051,
)
