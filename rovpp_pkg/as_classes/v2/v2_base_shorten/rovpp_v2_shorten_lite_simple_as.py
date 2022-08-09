from bgp_simulator_pkg import Relationships

from ..v2_base import ROVPPV2LiteSimpleAS


class ROVPPV2ShortenLiteSimpleAS(ROVPPV2LiteSimpleAS):

    __slots__ = tuple()

    name = "ROV++V2 Shorten Lite Simple"

    def _copy_and_process(self,
                          ann,
                          recv_relationship,
                          overwrite_default_kwargs=None):
        """Deep copies ann and modifies attrs"""

        if overwrite_default_kwargs:
            overwrite_default_kwargs["holes"] = holes[ann]
        else:
            overwrite_default_kwargs = {"holes": holes[ann]}
        if ann.invalid_by_roa and not ann.preventive:
            overwrite_default_kwargs["as_path"] = tuple([ann.as_path[-1]])

        return super(ROVPPV2ShortenLiteSimpleAS, self)._copy_and_process(
            ann,
            recv_relationship,
            overwrite_default_kwargs=overwrite_default_kwargs)
