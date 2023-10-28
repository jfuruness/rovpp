from ..v2_base import ROVPPV2LiteSimpleAS


class ROVPPV2ShortenLiteSimpleAS(ROVPPV2LiteSimpleAS):
    name = "ROV++V2 Shorten Lite Simple"

    def _copy_and_process(self, ann, recv_relationship, overwrite_default_kwargs=None):
        """Deep copies ann and modifies attrs"""

        if overwrite_default_kwargs:
            overwrite_default_kwargs["holes"] = self.temp_holes[ann]
        else:
            overwrite_default_kwargs = {"holes": self.temp_holes[ann]}
        if ann.invalid_by_roa and not ann.preventive:
            # tuple([ann.as_path[-1]])
            overwrite_default_kwargs["as_path"] = tuple([self.asn])
            overwrite_default_kwargs["blackhole"] = True

        return super(ROVPPV2LiteSimpleAS, self)._copy_and_process(
            ann, recv_relationship, overwrite_default_kwargs=overwrite_default_kwargs
        )
