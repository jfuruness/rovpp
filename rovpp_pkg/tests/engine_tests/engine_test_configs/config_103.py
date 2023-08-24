from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_051
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS, ROVSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedSuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn


config_103 = EngineTestConfig(
    name="103",
    desc="Superprefix+Prefix Attack on NonRouted Prefix with ROV",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedSuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVSimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({4: ROVSimpleAS}),
        AnnCls=ROVPPAnn
    ),
    graph=graph_051,
    propagation_rounds=1
)
