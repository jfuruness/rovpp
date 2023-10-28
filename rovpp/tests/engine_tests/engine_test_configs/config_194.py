from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_016
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp import ROVPPAnn
from rovpp import ROVPPV2aSimpleAS

config_194 = EngineTestConfig(
    name="194",
    desc="Subprefix Hijack Attack with v2a",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2aSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({12: ROVPPV2aSimpleAS}),
    ),
    graph=graph_016,
    propagation_rounds=1,
)
