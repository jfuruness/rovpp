from .rovpp_v2_lite_policy import ROVPPV2LitePolicy

class ROVPPV2aLitePolicy(ROVPPV2LitePolicy):

    name = "ROV++V2a Lite"

    def _policy_propagate(*args, **kwargs):
        """Do nothing. Send blackholes according to export policy"""

        return False
