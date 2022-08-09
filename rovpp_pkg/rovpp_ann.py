import dataclasses

from bgp_simulator_pkg import Announcement


@dataclasses.dataclass(eq=False, unsafe_hash=True)
class ROVPPAnn(Announcement):
    __slots__ = ("holes", "blackhole", "preventive", "attacker_on_route")

    holes: tuple
    blackhole: bool
    preventive: bool
    attacker_on_route: bool
