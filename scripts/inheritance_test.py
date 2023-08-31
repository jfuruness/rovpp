# Doing this to test if dataclasses inherit __hash___
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

    def __hash__(self):
        return hash(str(self))

    def __to_yaml_dict__(self):
        """This optional method is called when you call yaml.dump()

        We need to overwrite this from the base class because the holes attr
        contains a dictionary so we need to do this
        """

        dct = asdict(self)
        return frozendict(dct)


@yaml_info(yaml_tag="ROVPPAnn")
@dataclass(slots=True, frozen=True)
class ROVPPAnn2(Announcement):
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


a = ROVPPAnn(
    prefix="1",
    as_path=(1,),
    timestamp=0,
    seed_asn=0,
    roa_valid_length=True,
    roa_origin=0,
    recv_relationship=None,
)
b = ROVPPAnn(
    prefix="1",
    as_path=(1,),
    timestamp=0,
    seed_asn=0,
    roa_valid_length=True,
    roa_origin=0,
    recv_relationship=None,
)
assert hash(a) == hash(b)
