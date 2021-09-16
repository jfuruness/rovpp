from copy import deepcopy

from ipaddress import ip_network

from lib_bgp_simulator import BGPPolicy, IncomingAnns, ROAValidity, Relationships

from .blackhole import Blackhole
from .rovpp_v1_lite_policy import ROVPPV1LitePolicy


class ROVPPV2LitePolicy(ROVPPV1LitePolicy):

    name = "ROV++V2 Lite"

    def _propagate(policy_self, self, propagate_to, send_rels: list):
        """Propogates announcements from local rib to other ASes

        send_rels is the relationships that are acceptable to send

        Later you can change this so it's not the local rib that's
        being sent. But this is just proof of concept.
        """

        for as_obj in getattr(self, propagate_to.name.lower()):
            for prefix, ann in policy_self.local_rib.items():
                if ann.recv_relationship in send_rels:
                    if isinstance(ann, Blackhole):
                        if (ann.recv_relationship in [Relationships.PEERS, Relationships.PROVIDERS]
                            and propagate_to == Relationships.CUSTOMERS):
                            as_obj.policy.incoming_anns[prefix].append(ann)
                    else:
                        # Add the new ann to the incoming anns for that prefix
                        as_obj.policy.incoming_anns[prefix].append(ann)
