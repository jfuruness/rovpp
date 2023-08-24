from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_048
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, NonRoutedSuperprefixHijack

from rovpp_pkg import ROVPPAnn, ROVPPV2SimpleAS


config_085 = EngineTestConfig(
    name="085",
    desc="Superprefix Attack on NonRouted Prefix with v2",
    scenario_config=ScenarioConfig(
        ScenarioCls=NonRoutedSuperprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2SimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({
            3: ROVPPV2SimpleAS,
            4: ROVPPV2SimpleAS,
            6: ROVPPV2SimpleAS,
        }),
        AnnCls=ROVPPAnn
    ),
    graph=graph_048,
)
