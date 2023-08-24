from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_037
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPAnn
from rovpp_pkg import ROVPPV2aSimpleAS

config_178 = EngineTestConfig(
    name="178",
    desc="Subprefix Hijack Attack with v2a",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2aSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({1: ROVPPV2aSimpleAS, 11: ROVPPV2aSimpleAS, 12: ROVPPV2aSimpleAS, 5: ROVPPV2aSimpleAS, 6: ROVPPV2aSimpleAS, ASNs.VICTIM.value: ROVPPV2aSimpleAS})
    ),
    graph=graph_037,
    propagation_rounds=1
)
