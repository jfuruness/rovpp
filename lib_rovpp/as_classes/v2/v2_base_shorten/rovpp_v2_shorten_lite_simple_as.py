from lib_bgp_simulator import Relationships

from ..v2_base import ROVPPV2LiteSimpleAS


class ROVPPV2ShortenLiteSimpleAS(ROVPPV2LiteSimpleAS):

    __slots__ = tuple()

    name = "ROV++V2 Shorten Lite Simple"


    def _copy_and_process(self,
                          ann,
                          recv_relationship,
                          holes=None,
                          **extra_kwargs):
        """Deep copies ann and modifies attrs"""

        
        # if ann.invalid_by_roa and not ann.preventive:
        #     extra_kwargs["blackhole"] = True
        #     extra_kwargs["traceback_end"] = True
        extra_kwargs["holes"] = holes[ann]
        extra_kwargs["as_path"] = tuple([ann.as_path[-1]])
        return super(ROVPPV2ShortenLiteSimpleAS, self)._copy_and_process(
                     ann, recv_relationship, **extra_kwargs)
