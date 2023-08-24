from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_049
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedPrefixHijack

from rovpp_pkg import ROVPPAnn, ROVPPV2SimpleAS


config_081 = EngineTestConfig(
    name="081",
    desc="NonRouted Prefix Hijack with v2",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2SimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            4: ROVPPV2SimpleAS,
        }),
        AnnCls=ROVPPAnn
    ),
    graph=graph_049,
)
