from dataclasses import dataclass
from itertools import chain

from lib_bgp_simulator import Announcement

@dataclass(eq=False)
class ROVPPAnn(Announcement):
    __slots__ = ["holes", "blackhole", "temp_holes"]

    holes: list
    blackhole: bool
    temp_holes: list
