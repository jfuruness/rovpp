from frozendict import frozendict

from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SuperprefixPrefixHijack

from rovpp import ROVPPAnn, ROVPPV1SimpleAS

# from bgpy import ROVSimpleAS

from .config_221_goal_1 import counter_ex_graph

config_222 = EngineTestConfig(
    name="222 (Do no harm ROV)",
    desc="ROV++ nodes are disconnected (when ROV would have connected)",
    scenario_config=ScenarioConfig(
        ScenarioCls=SuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1SimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                2: ROVPPV1SimpleAS,
                5: ROVPPV1SimpleAS,
            }
        ),
    ),
    graph=counter_ex_graph,
    propagation_rounds=1,
)
