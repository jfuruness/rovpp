from dataclasses import dataclass
from itertools import chain

from lib_bgp_simulator import Announcement

@dataclass(eq=False)
class ROVPPAnn(Announcement):
    __slots__ = ["holes", "blackhole", "temp_holes", "preventive",
                 "attacker_on_route"]

    holes: list
    blackhole: bool
    temp_holes: list
    preventive: bool
    attacker_on_route: bool
