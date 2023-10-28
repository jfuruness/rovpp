from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_016
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SuperprefixPrefixHijack

from rovpp import ROVPPAnn, ROVPPV2aSimpleAS


config_064 = EngineTestConfig(
    name="064",
    desc=(
        "This is running as single adopting AS (ROV++ v2a AS 12).\n"
        "This is 22 AS topology "
        "with a clique at the top with 1,2,3, and 4.\nIts about 4 levels "
        "tall.\nThe attacker under the same provider as the legitmated "
        "origin\n(i.e. they’re both on the edge next to each other)."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=SuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2aSimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({12: ROVPPV2aSimpleAS}),
        AnnCls=ROVPPAnn,
    ),
    graph=graph_016,
)
