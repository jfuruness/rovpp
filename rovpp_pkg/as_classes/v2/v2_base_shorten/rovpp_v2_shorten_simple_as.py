from lib_bgp_simulator import Relationships

from ..v2_base import ROVPPV2SimpleAS


class ROVPPV2ShortenSimpleAS(ROVPPV2SimpleAS):

    __slots__ = tuple()

    name = "ROV++V2 Shorten Simple"


    def _copy_and_process(self,
                          ann,
                          recv_relationship,
                          holes=None,
                          **extra_kwargs):
        """Deep copies ann and modifies attrs"""

        
        # if ann.invalid_by_roa and not ann.preventive:
        #     extra_kwargs["blackhole"] = True
        #     extra_kwargs["traceback_end"] = True
        # These anns will be blackholes
        if ann.invalid_by_roa and not ann.preventive:
            extra_kwargs["as_path"] = tuple([ann.as_path[-1]])
        return super(ROVPPV2ShortenSimpleAS, self)._copy_and_process(
                     ann, recv_relationship, holes=holes, **extra_kwargs)
