from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_005
from bgpy.tests.engine_tests.utils import EngineTestConfig
from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPV2SimpleAS, ROVPPAnn

config_044 = EngineTestConfig(
    name="044",
    desc="Subprefix Hijack from fig 4 in paper with ROV++ v2",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2SimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({5: ROVPPV2SimpleAS}),
    ),
    graph=graph_005,
)
