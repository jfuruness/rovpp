from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_039
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPAnn, ROVPPV1LiteSimpleAS


config_072 = EngineTestConfig(
    name="072",
    desc=(
        "ROV++ v1 lite adopting\n"
        "Example where v2 leads to a higher disconnection "
        "rate\nand lower successful connection rate\n"
        "(for nonadopting ASes)."
        "When AS 33 adopts v2,\nit sends a blackhole announcement to "
        "AS 3,\nwhich will be further forwarded to AS 3’s customer"
        "cone.\nWhen AS 33 adopts v1,\nit only sets up a local "
        "blackhole.\nAS 3 only receives one announcement (1.2/16) "
        "from AS 1\nand"
        "no other announcement.\nIt will hence route traffic destining "
        "to 1.2.3/24 via AS 1 to the legit origin, AS 5.\n"
        "Similarly, AS 3’s "
        "customers’ traffic to 1.2.3/24 will be routed successfully.\n"
        "In the figure,\nwhether AS 5 adopts ROV++ or not doesn't matter\n"
        "since the hijack announcement will not be sent out by "
        "AS 5 to AS 1 anyway\n(due to valley-free routing)."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1LiteSimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({33: ROVPPV1LiteSimpleAS}),
        AnnCls=ROVPPAnn,
    ),
    graph=graph_039,
)
