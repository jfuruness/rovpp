import dataclasses
from itertools import chain

from lib_bgp_simulator import Announcement

@dataclasses.dataclass(eq=False)
class ROVPPAnn(Announcement):
    __slots__ = ["holes", "blackhole", "temp_holes", "preventive",
                 "attacker_on_route"]

    holes: list
    blackhole: bool
    temp_holes: list
    preventive: bool
    attacker_on_route: bool

    def __eq__(self, other):
        if isinstance(other, Announcement):
            self_dict = dataclasses.asdict(self)
            other_dict = dataclasses.asdict(other)
            # Doing this because list order can change
            # TODO: fix later
            for key in ["holes", "temp_holes"]:
                for dct in self_dict, other_dict:
                    dct.pop(key)
            return self_dict == other_dict
        else:
            return NotImplemented

