from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_006
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedPrefixHijack

from rovpp_pkg import ROVPPV1SimpleAS, ROVPPAnn


config_051 = EngineTestConfig(
    name="051",
    desc=(
        "Prefix hijack on a non-routed prefix. Here adopting AS 2 is "
        "adopting ROV++ v1, and should detect the attack and create "
        "a local blackhole for itself and disconnect its customer."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1SimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({2: ROVPPV1SimpleAS}),
        AnnCls=ROVPPAnn
    ),
    graph=graph_006,
)
