from bgp_simulator_pkg import Announcement


class ROVPPAnn(Announcement):

    __slots__ = ("holes", "blackhole", "preventive", "attacker_on_route")

    def __init__(self,
                 *args,
                 holes=(),
                 blackhole: bool = False,
                 preventive: bool = False,
                 attacker_on_route: bool = False,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.holes = holes
        self.blackhole: bool = blackhole
        # V3 only
        self.preventive: bool = preventive
        # V3 only
        self.attacker_on_route: bool = attacker_on_route
