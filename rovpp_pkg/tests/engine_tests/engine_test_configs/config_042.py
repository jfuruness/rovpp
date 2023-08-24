from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_004
from bgpy.tests.engine_tests.utils import EngineTestConfig
from bgpy.simulation_engine import BGPSimpleAS, ROVSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPV2aLiteSimpleAS, ROVPPAnn

config_042 = EngineTestConfig(
    name="042",
    desc=("Subprefix Hijack from fig 3a in paper with ROV++ v2a lite "
          "adopting at AS 4 and 8, and ROV at 7. "
          "ASes 4, 8, and 7 should be disconnected"),
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2aLiteSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {4: ROVPPV2aLiteSimpleAS, 7: ROVSimpleAS, 8: ROVPPV2aLiteSimpleAS}
        ),
    ),
    graph=graph_004,
)
