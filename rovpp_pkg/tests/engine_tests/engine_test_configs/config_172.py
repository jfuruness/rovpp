from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_036
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV1SimpleAS

config_172 = EngineTestConfig(
    name="172",
    desc="Subprefix Hijack Attack with v1",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1SimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                5: ROVPPV1SimpleAS,
                8: ROVPPV1SimpleAS,
                10: ROVPPV1SimpleAS,
                15: ROVPPV1SimpleAS,
                ASNs.VICTIM.value: ROVPPV1SimpleAS,
            }
        ),
    ),
    graph=graph_036,
    propagation_rounds=1,
)
