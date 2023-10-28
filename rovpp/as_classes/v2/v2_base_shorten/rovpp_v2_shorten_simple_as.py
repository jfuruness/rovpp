from ..v2_base import ROVPPV2SimpleAS


class ROVPPV2ShortenSimpleAS(ROVPPV2SimpleAS):
    name = "ROV++V2 Shorten Simple"

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

        return super(ROVPPV2SimpleAS, self)._copy_and_process(
            ann, recv_relationship, overwrite_default_kwargs=overwrite_default_kwargs
        )
