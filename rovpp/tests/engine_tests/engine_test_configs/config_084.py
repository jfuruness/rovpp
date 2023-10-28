from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_048
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedSuperprefixHijack

from rovpp import ROVPPAnn, ROVPPV1SimpleAS


config_084 = EngineTestConfig(
    name="084",
    desc="Superprefix Attack on NonRouted Prefix with v1",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedSuperprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1SimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                3: ROVPPV1SimpleAS,
                4: ROVPPV1SimpleAS,
                6: ROVPPV1SimpleAS,
            }
        ),
        AnnCls=ROVPPAnn,
    ),
    graph=graph_048,
)
