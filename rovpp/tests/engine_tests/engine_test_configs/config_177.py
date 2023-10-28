from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_037
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp import ROVPPAnn
from rovpp import ROVPPV2SimpleAS

config_177 = EngineTestConfig(
    name="177",
    desc="Subprefix Hijack Attack with v2",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2SimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                1: ROVPPV2SimpleAS,
                11: ROVPPV2SimpleAS,
                12: ROVPPV2SimpleAS,
                5: ROVPPV2SimpleAS,
                6: ROVPPV2SimpleAS,
                ASNs.VICTIM.value: ROVPPV2SimpleAS,
            }
        ),
    ),
    graph=graph_037,
    propagation_rounds=1,
)
