from itertools import chain

from lib_bgp_simulator import Announcement


class ROVPPAnn(Announcement):
    __slots__ = ["holes", "blackhole", "temp_holes"]

    def __init__(self, *args, blackhole=False, **kwargs):
        """Inits ann and adds blackhole and invalid subprefixes"""

        self.blackhole = blackhole
        # Subprefix includes itself
        # Invalid subprefixes from same neighbor
        self.holes = kwargs.pop("holes", [])
        temp_holes = kwargs.pop("temp_holes", None)
        if temp_holes is not None:
            self.temp_holes = temp_holes

        super(ROVPPAnn, self).__init__(*args, **kwargs)

    @property
    def default_copy_kwargs(self):

        # Gets all slots from parent classes and this class
        # https://stackoverflow.com/a/6720815/8903959
        slots = set(chain.from_iterable(getattr(cls, '__slots__', [])
                                            for cls in self.__class__.__mro__))
        if not hasattr(self, "temp_holes"):
            slots.remove("temp_holes")

        kwargs = {attr: getattr(self, attr) for attr in slots}
        kwargs["seed_asn"] = None
        kwargs["traceback_end"] = False
        return kwargs
