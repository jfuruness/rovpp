from dataclasses import dataclass
from typing import Tuple

from yamlable import yaml_info

from bgpy import Announcement


@yaml_info(yaml_tag="ROVPPAnn")
@dataclass(slots=True, frozen=True)
class ROVPPAnn(Announcement):
    holes: Tuple[str] = ()
    blackhole: bool = False
    preventive: bool = False
    attacker_on_route: bool = False

    # I think this might be redundant since this is in the parent class
    # But I'm not 100% sure so just to avoid errors transitioning to BGPy
    # I'm adding it here (Aug 17 2023)
    def __hash__(self):
        return hash(str(self))
