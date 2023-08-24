from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_049
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedSuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn
from bgpy import ROVSimpleAS


config_107 = EngineTestConfig(
    name="107",
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
    graph=graph_049,
    propagation_rounds=1
)
