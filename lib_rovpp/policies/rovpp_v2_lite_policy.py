from copy import deepcopy

from ipaddress import ip_network

from lib_bgp_simulator import ROAValidity, Relationships

from .rovpp_v1_lite_policy import ROVPPV1LitePolicy


class ROVPPV2LitePolicy(ROVPPV1LitePolicy):

    __slots__ = []

    name = "ROV++V2 Lite"

    def _policy_propagate(self, neighbor, ann, propagate_to, send_rels):
        """Deals with blackhole propagation

        If ann is a blackhole, it must be recv from peers/providers and must
        be sent only to customers
        """

        if ann.blackhole:
            if _send_competing_hijack_allowed(ann, propagate_to):
                self._process_outgoing_ann(neighbor, ann, propagate_to, send_rels)
            return True

    def _send_competing_hijacked_allowed(self, ann, propagate_to):
        return (ann.recv_relationship in [Relationships.PEERS, Relationships.PROVIDERS]
                and propagate_to == Relationships.CUSTOMERS)
