from ..v2_base import ROVPPV2LiteSimpleAS


class ROVPPV2aLiteSimpleAS(ROVPPV2LiteSimpleAS):

    name = "ROV++V2a Lite Simple"

    def _policy_propagate(*args, **kwargs):
        """Do nothing. Send blackholes according to export policy"""

        return False
