from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_006
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS, ROVSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedPrefixHijack

from rovpp_pkg import ROVPPAnn


config_050 = EngineTestConfig(
    name="050",
    desc=(
        "Prefix hijack on a non-routed prefix. Here adopting AS 2 is "
        "adopting ROV, and should be able to detect the attack and "
        "drop the hijack ann, hence disconnecting itself and customer."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVSimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({2: ROVSimpleAS}),
        AnnCls=ROVPPAnn,
    ),
    graph=graph_006,
)
