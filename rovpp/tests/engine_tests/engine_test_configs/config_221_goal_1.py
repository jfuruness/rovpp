from frozendict import frozendict

from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SuperprefixPrefixHijack

from rovpp import ROVPPAnn  # , ROVPPV1SimpleAS
from bgpy import ROVSimpleAS
from bgpy import GraphInfo
from bgpy.caida_collector import CustomerProviderLink as CPLink, PeerLink


counter_ex_graph = GraphInfo(
    peer_links=set(
        {
            PeerLink(2, 3),
        }
    ),
    customer_provider_links=set(
        [
            CPLink(provider_asn=1, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=2, customer_asn=ASNs.ATTACKER.value),
            CPLink(provider_asn=3, customer_asn=ASNs.VICTIM.value),
            CPLink(provider_asn=4, customer_asn=1),
            CPLink(provider_asn=5, customer_asn=4),
            CPLink(provider_asn=5, customer_asn=2),
        ]
    ),
    diagram_ranks=[
        [1, ASNs.ATTACKER.value, ASNs.VICTIM.value],
        [4, 2, 3],
        [5],
    ],
)

config_221 = EngineTestConfig(
    name="221 (Do no harm ROV)",
    desc="ROV nodes are successfully connected",
    scenario_config=ScenarioConfig(
        ScenarioCls=SuperprefixPrefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVSimpleAS,
        AnnCls=ROVPPAnn,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict(
            {
                2: ROVSimpleAS,
                5: ROVSimpleAS,
            }
        ),
    ),
    graph=counter_ex_graph,
    propagation_rounds=1,
)
