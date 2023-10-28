from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_003
from bgpy.tests.engine_tests.utils import EngineTestConfig
from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp import ROVPPV1SimpleAS, ROVPPAnn

config_037 = EngineTestConfig(
    name="rovpp_037",
    desc="Subprefix Hijack from fig 2 in paper with ROV++ v1 adopting.",
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1SimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {3: ROVPPV1SimpleAS, 4: ROVPPV1SimpleAS}
        ),
    ),
    graph=graph_003,
)
