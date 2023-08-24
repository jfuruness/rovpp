from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_013
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn, ROVPPV2aSimpleAS

config_138 = EngineTestConfig(
    name="138",
    desc="Superprefix+Prefix Attack on Prefix with v2a",
    scenario_config=ScenarioConfig(
        ScenarioCls=SuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2aSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({2: ROVPPV2aSimpleAS})
    ),
    graph=graph_013,
    propagation_rounds=1
)
