from lib_bgp_simulator import Announcement


class ROVPPAnn(Announcement):
    __slots__ = ["invalid_subprefixes_from_same_neighbor", "blackhole"]

    def __init__(self, *args, blackhole=False, **kwargs):
        """Inits ann and adds blackhole and invalid subprefixes"""

        super(ROVPPAnn, self).__init__(*args, **kwargs)
        self.blackhole = blackhole
        # Subprefix includes itself
        self.invalid_subprefixes_from_same_neighbor = 0

    def copy_w_sim_attrs(self, cls=None, **extra_kwargs):
        """Copies sim attrs"""

        kwargs = {"blackhole": self.blackhole,
                  "invalid_subprefixes_from_same_neighbor":
                        self.invalid_subprefixes_from_same_neighbor}

        kwargs.update(extra_kwargs)

        cls = cls if cls else self.__class__

        return super(ROVPPAnn, self).copy_w_sim_attrs(cls=cls, **kwargs)
