from dataclasses import dataclass, asdict
from typing import Tuple

from frozendict import frozendict
from yamlable import yaml_info

from bgpy import Announcement


@yaml_info(yaml_tag="ROVPPAnn")
@dataclass(slots=True, frozen=True)
class ROVPPAnn(Announcement):
    holes: Tuple[str] = ()
    blackhole: bool = False
    preventive: bool = False
    attacker_on_route: bool = False

    def __to_yaml_dict__(self):
        """This optional method is called when you call yaml.dump()

        We need to overwrite this from the base class because the holes attr
        contains a dictionary so we need to do this
        """

        dct = asdict(self)
        return frozendict(dct)
