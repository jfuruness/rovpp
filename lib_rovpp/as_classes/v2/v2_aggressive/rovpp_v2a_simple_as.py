from ..v2_base import ROVPPV2SimpleAS

class ROVPPV2aSimpleAS(ROVPPV2SimpleAS):

    __slots__ = []

    name = "ROV++V2a Simple"

    def _policy_propagate(*args, **kwargs):
        """Do nothing. Send blackholes according to export policy"""

        return False
