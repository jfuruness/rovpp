from frozendict import frozendict

from bgpy.tests.engine_tests.graphs import graph_039
from bgpy.tests.engine_tests.utils import EngineTestConfig

from bgpy.simulation_engine import BGPSimpleAS
from bgpy.enums import ASNs
from bgpy.simulation_framework import ScenarioConfig, SubprefixHijack

from rovpp_pkg import ROVPPAnn, ROVPPV1SimpleAS


config_073 = EngineTestConfig(
    name="073",
    desc=(
        "ROV++ v1 adopting\n"
        "Example where v2 leads to a higher disconnection "
        "rate\nand lower successful connection rate\n"
        "(for nonadopting ASes).\n"
        "When AS 33 adopts v2,\nit sends a blackhole announcement to "
        "AS 3,\nwhich will be further forwarded to AS 3’s customer"
        "cone.\nWhen AS 33 adopts v1,\nit only sets up a local "
        "blackhole.\nAS 3 only receives one announcement (1.2/16) "
        "from AS 1 and"
        "no other announcement.\nIt will hence route traffic destining "
        "to 1.2.3/24 via AS 1\n to the legit origin, AS 5.\n"
        "Similarly, AS 3’s "
        "customers’ traffic to 1.2.3/24 will be routed successfully.\n"
        "In the figure,\nwhether AS 5 adopts ROV++ or not doesn't matter\n"
        "since the hijack announcement will not be sent out by "
        "AS 5 to AS 1 anyway\n(due to valley-free routing)."
    ),
    scenario_config=ScenarioConfig(
        ScenarioCls=SubprefixHijack,
        BaseASCls=BGPSimpleAS,
        AdoptASCls=ROVPPV1SimpleAS,
        override_attacker_asns=frozenset({ASNs.ATTACKER.value}),
        override_victim_asns=frozenset({ASNs.VICTIM.value}),
        override_non_default_asn_cls_dict=frozendict({33: ROVPPV1SimpleAS}),
        AnnCls=ROVPPAnn,
    ),
    graph=graph_039,
)
