#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink

from .run_example import run_example

from lib_bgp_simulator.enums import ASNs, Prefixes, Timestamps, ROAValidity, Relationships
# from lib_bgp_simulator.announcement import Announcement
from ..attacks.rovpp_ann import ROVPPAnn

__author__ = "Reynaldo"
__credits__ = ["Reynaldo Morillo"]
__Lisence__ = "BSD"
__maintainer__ = "Reynaldo Morillo"
__email__ = "reynaldo.morillo@uconn.edu"
__status__ = "Development"

#######################################
# (Remapping) Constants
#######################################

# Remapping
victim_asn = ASNs.VICTIM.value
attacker_asn = ASNs.ATTACKER.value
prefix_val = Prefixes.PREFIX.value 
subprefix_val = Prefixes.SUBPREFIX.value
superprefix_val = Prefixes.SUPERPREFIX.value

# Define Attacker and victim
vic_kwargs = {"prefix": prefix_val,
              "timestamp": Timestamps.VICTIM.value,
              "seed_asn": None,
              "roa_validity": ROAValidity.VALID,
              "withdraw": False,
              "traceback_end": False,
              "holes": None,
              "blackhole": False,
              "temp_holes": None}
atk_kwargs = {"prefix": subprefix_val,
              "timestamp": Timestamps.ATTACKER.value,
              "seed_asn": None,
              "roa_validity": ROAValidity.INVALID,
              "withdraw": False,
              "traceback_end": False,
              "holes": None,
              "blackhole": False,
              "temp_holes": None}
atk_superprefix_kwargs = {"prefix": superprefix_val,
              "timestamp": Timestamps.ATTACKER.value,
              "seed_asn": None,
              "roa_validity": ROAValidity.INVALID,
              "withdraw": False,
              "traceback_end": False,
              "holes": None,
              "blackhole": False,
              "temp_holes": None}


victim_or_attacker_kwargs = {
    prefix_val      : vic_kwargs,
    subprefix_val   : atk_kwargs,
    superprefix_val : atk_superprefix_kwargs
}


#######################################
# Helper Functions
#######################################

def create_local_ribs(exr_output):
    local_ribs = dict()
    for i in range(len(exr_output)):
        # Extract announcement attributes
        asn = exr_output[i]["asn"]
        ann_prefix = exr_output[i]["prefix"]
        path = exr_output[i]["as_path"]
        relationship = exr_output[i]["recv_relationship"]
        is_blackhole = exr_output[i]["blackhole"] if "blackhole" in exr_output[i] else False
        ribs = local_ribs[asn] if asn in local_ribs else None
        kwargs_added = True if "kwargs" in exr_output else False
        # Create LocalRib items
        if ribs is None:
            # Create a new LocalRib
            ribs = {ann_prefix: ROVPPAnn(as_path=path,
                                         recv_relationship=relationship,
                                         **exr_output[i].get("kwargs", victim_or_attacker_kwargs[ann_prefix]))
                   }
        else:
            # Add to existing LocalRib
            ribs[ann_prefix] = ROVPPAnn(as_path=path,
                                        recv_relationship=relationship,
                                        **exr_output[i].get("kwargs", victim_or_attacker_kwargs[ann_prefix]))
        # Update local_ribs
        local_ribs[asn] = ribs

        # Add blackhole if is_blackhole
        if is_blackhole:
            local_ribs[asn][ann_prefix].blackhole=True
            local_ribs[asn][ann_prefix].traceback_end=True
            
    return local_ribs


