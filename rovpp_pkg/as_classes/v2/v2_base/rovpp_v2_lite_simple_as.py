from bgp_simulator_pkg import Relationships

from ...v1 import ROVPPV1LiteSimpleAS


class ROVPPV2LiteSimpleAS(ROVPPV1LiteSimpleAS):

    __slots__ = tuple()

    name = "ROV++V2 Lite Simple"

    def _policy_propagate(self, neighbor, ann, propagate_to, *args):
        """Deals with blackhole propagation

        If ann is a blackhole, it must be recv from peers/providers and must
        be sent only to customers
        """

        # If blackhole and subprefix or non-routed
        if ann.blackhole:
            if self._send_competing_hijack_allowed(ann, propagate_to):
                self._process_outgoing_ann(neighbor, ann, propagate_to, *args)
            return True
        else:
            return False

    def _send_competing_hijack_allowed(self, ann, propagate_to):
        return (ann.recv_relationship in [Relationships.PEERS,
                                          Relationships.PROVIDERS,
                                          Relationships.ORIGIN,]
                and propagate_to == Relationships.CUSTOMERS
                and (not ann.roa_valid_length or not ann.roa_routed))
