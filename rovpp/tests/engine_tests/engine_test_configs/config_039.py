from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_004
from bgpy.tests.engine_tests.utils import EngineTestConfig
from bgpy.simulation_engine import BGPSimpleAS, ROVSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp import ROVPPV1SimpleAS, ROVPPAnn

config_039 = EngineTestConfig(
    name="rovpp_039",
    desc=(
        "Subprefix Hijack from fig 3a in paper with "
        "ROV++ v1 adopting at AS 4, and ROV at 7 and 8."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1SimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {4: ROVPPV1SimpleAS, 7: ROVSimpleAS, 8: ROVSimpleAS}
        ),
    ),
    graph=graph_004,
)
