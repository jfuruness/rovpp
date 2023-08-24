from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_011
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPAnn
from bgpy.tests.bgpy_tests.base_classes import ROVPPV1SimpleAS

config_180 = EngineTestConfig(
    name="180",
    desc="Subprefix Hijack Attack with v1",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1SimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({5: ROVPPV1SimpleAS, 6: ROVPPV1SimpleAS, 1: ROVPPV1SimpleAS, 11: ROVPPV1SimpleAS, 12: ROVPPV1SimpleAS})
    ),
    graph=graph_011,
    propagation_rounds=1
)
