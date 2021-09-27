from lib_bgp_simulator import Announcement


class ROVPPAnn(Announcement):
    __slots__ = ["holes", "blackhole"]

    def __init__(self, *args, blackhole=False, **kwargs):
        """Inits ann and adds blackhole and invalid subprefixes"""

        self.blackhole = blackhole
        # Subprefix includes itself
        # Invalid subprefixes from same neighbor
        self.holes = kwargs.pop("holes", [])

        super(ROVPPAnn, self).__init__(*args, **kwargs)
