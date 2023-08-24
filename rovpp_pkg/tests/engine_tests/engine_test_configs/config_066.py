from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_010
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn, ROVPPV1SimpleAS


config_066 = EngineTestConfig(
    name="066",
    desc="ROV++ v1 adopting AS 2. It is not useful in this type of attack",
    scenario_config=ScenarioConfig(
        ScenarioCls=SuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1SimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({2: ROVPPV1SimpleAS}),
        AnnCls=ROVPPAnn,
    ),
    graph=graph_010,
)
