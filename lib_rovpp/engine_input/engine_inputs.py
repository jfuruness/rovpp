from lib_bgp_simulator import PrefixHijack
from lib_bgp_simulator import SubprefixHijack
from lib_bgp_simulator import NonRoutedPrefixHijack
from lib_bgp_simulator import SuperprefixPrefixHijack
from lib_bgp_simulator import NonRoutedSuperprefixHijack

from .rovpp_engine_input import ROVPPEngineInput


"""All ROV++ Engine inputs. Nothing else is compatible"""


class ROVPPPrefixHijack(ROVPPEngineInput, PrefixHijack):
    pass


class ROVPPNonRoutedPrefixHijack(ROVPPEngineInput, NonRoutedPrefixHijack):
    pass


class ROVPPNonRoutedSuperprefixHijack(ROVPPEngineInput,
                                      NonRoutedSuperprefixHijack):
    pass


class ROVPPSuperprefixPrefixHijack(ROVPPEngineInput, SuperprefixPrefixHijack):
    pass


class ROVPPSubprefixHijack(ROVPPEngineInput, SubprefixHijack):
    pass
