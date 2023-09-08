from bgpy import Relationships

from ..v2_base import ROVPPV2LiteSimpleAS


class ROVPPV2JournalLiteSimpleAS(ROVPPV2LiteSimpleAS):
    name = "ROV++V2 Journal Lite Simple"

    def _send_competing_hijack_allowed(self, ann, propagate_to):
        return (
            # Commenting this out, since Journal version also can get from customer
            # ann.recv_relationship
            # in [Relationships.PEERS, Relationships.PROVIDERS, Relationships.ORIGIN]
            # and propagate_to == Relationships.CUSTOMERS
            propagate_to == Relationships.CUSTOMERS
            and (not ann.roa_valid_length or not ann.roa_routed)
        )
