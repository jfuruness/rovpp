from frozendict import frozendict
from bgpy.tests.engine_tests.graphs import graph_012
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SuperprefixPrefixHijack

from rovpp import ROVPPAnn, ROVPPV2aSimpleAS

config_130 = EngineTestConfig(
    name="130",
    desc="Superprefix+Prefix Attack on Prefix with v2a",
    scenario_config=ScenarioConfig(
        ScenarioCls=SuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2aSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {2: ROVPPV2aSimpleAS, 4: ROVPPV2aSimpleAS, 11: ROVPPV2aSimpleAS}
        ),
    ),
    graph=graph_012,
    propagation_rounds=1,
)
