from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_022
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPAnn, ROVPPV2SimpleAS


config_058 = EngineTestConfig(
    name="058",
    desc=(
        "This is a v2 test.\nA suggested test for v2 versus v2a. "
        "v2a leads to additional "
        "benefits over v2.\nWhen AS 4 uses v2, AS 7 and its customer cone "
        "will be hijacked.\nWhen AS 4 uses v2a, the blackhole announcement"
        " from AS 4 will compete with the hijack announcement.\nIn this "
        "case, AS 7 will choose the blackhole announcement,\nand hence "
        "AS 7 and its customer cone\nwill be will be disconnected "
        "instead of hijacked."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV2SimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({4: ROVPPV2SimpleAS}),
        AnnCls=ROVPPAnn
    ),
    graph=graph_022,
)
