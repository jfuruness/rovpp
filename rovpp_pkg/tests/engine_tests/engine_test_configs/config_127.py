from frozendict import frozendict
from bgpy.tests.engine_tests.graphs import graph_012
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS, ROVSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SuperprefixPrefixHijack

from rovpp_pkg import ROVPPAnn

config_127 = EngineTestConfig(
    name="127",
    desc="Superprefix+Prefix Attack on Prefix with ROV",
    scenario_config=ScenarioConfig(
        ScenarioCls=SuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {2: ROVSimpleAS, 4: ROVSimpleAS, 11: ROVSimpleAS}
        ),
    ),
    graph=graph_012,
)
