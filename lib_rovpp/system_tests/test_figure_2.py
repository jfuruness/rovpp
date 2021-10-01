#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains system tests for the extrapolator.

For speciifics on each test, see the docstrings under each function.
"""
import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink

from .run_example import run_example

from lib_bgp_simulator.enums import ASNs, Prefixes, Timestamps, ROAValidity, Relationships
from lib_bgp_simulator.simulator.attacks import SubprefixHijack
from lib_bgp_simulator.engine import LocalRib
from lib_bgp_simulator.engine.bgp_policy import BGPPolicy
from lib_bgp_simulator.engine.bgp_ribs_policy import BGPRIBSPolicy
from lib_bgp_simulator.announcement import Announcement
from lib_bgp_simulator.engine.rov_policy import ROVPolicy
from ..policies.rovpp_v1_lite_policy import ROVPPV1LitePolicy
from ..policies.rovpp_v1_policy import ROVPPV1Policy

__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness", "Reynaldo Morillo"]
__Lisence__ = "BSD"
__maintainer__ = "Justin Furuness"
__email__ = "jfuruness@gmail.com"
__status__ = "Development"


#######################################
# (Remapping) Constants
#######################################

# Remapping
victim_asn = ASNs.VICTIM.value
attacker_asn = ASNs.ATTACKER.value
prefix_val = Prefixes.PREFIX.value 
subprefix_val = Prefixes.SUBPREFIX.value

# Define Attacker and victim
vic_kwargs = {"prefix": prefix_val,
              "timestamp": Timestamps.VICTIM.value,
              "seed_asn": None,
              "roa_validity": ROAValidity.VALID}
atk_kwargs = {"prefix": subprefix_val,
              "timestamp": Timestamps.ATTACKER.value,
              "seed_asn": None,
              "roa_validity": ROAValidity.INVALID}


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
            last_asn_on_path = path[len(path)-1]
            ribs = local_ribs[asn] if asn in local_ribs else None
            # Create LocalRib items
            if ribs is None:
                # Create a new LocalRib
                if last_asn_on_path == victim_asn:
                    ribs = LocalRib({ann_prefix: Announcement(as_path=path,
                                                             recv_relationship=relationship,
                                                             **vic_kwargs)
                                   })
                elif last_asn_on_path == attacker_asn:
                    ribs = LocalRib({ann_prefix: Announcement(as_path=path,
                                                             recv_relationship=relationship,
                                                             **atk_kwargs)
                                               })
            else:
                # Add to existing LocalRib
                if last_asn_on_path == victim_asn:
                    ribs[ann_prefix] = Announcement(as_path=path,
                                                    recv_relationship=relationship,
                                                    **vic_kwargs)
                elif last_asn_on_path == attacker_asn:
                    ribs[ann_prefix] = Announcement(as_path=path,
                                                    recv_relationship=relationship,
                                                    **atk_kwargs)
            # Update local_ribs
            local_ribs[asn] = ribs

            # Add blackhole if is_blackhole
            if is_blackhole:
                local_ribs[asn][ann_prefix] = ribs[ann_prefix].copy(blackhole=True, traceback_end=True)
            
    return local_ribs


def run_topology(attack_type, adopt_policy, ribs):
    r"""v1 example with ROV

           44\ \
          /|  \ \
         / |   \ attacker_asn
        /  | 88 \
      77   | /\  \
      /    78  86 \
    11     |     \ \
           12     victim_asn
    """

    # Define Graph data
    peer_rows = []
    provider_customer_rows = [[44, attacker_asn],
                              [44, 77],
                              [44, 78],
                              [44, victim_asn],
                              [77, 11],
                              [78, 12],
                              [88, 78],
                              [88, 86],
                              [86, victim_asn]]
    customer_providers = [CPLink(provider_asn=x[0], customer_asn=x[1]) for x in provider_customer_rows]
    peers = [PeerLink(x[0], x[1]) for x in peer_rows]

    # Set adopting rows
    bgp_ases = [11, 44, 12, 88, 86, victim_asn, attacker_asn]
    adopting_ases = [77, 78]
    as_policies = dict()
    for bgp_as in bgp_ases:
        as_policies[bgp_as] = BGPRIBSPolicy
    for adopting_as in adopting_ases:
        as_policies[adopting_as] = adopt_policy
    
    # Create local ribs
    local_ribs = create_local_ribs(ribs)
    
    # Run test checks
    run_example(peers=peers,
                customer_providers=customer_providers,
                as_policies=as_policies,
                announcements=attack_type,
                local_ribs=local_ribs)


#######################################
# Tests
#######################################


class Test_Figure_2:
    """Tests all example graphs within our paper."""

    #@pytest.mark.skip(reason="Reynaldo working on it")
    def test_figure_2a(self):
        
        # Define Attack type and adoption policy
        attack_type = SubprefixHijack().announcements
        adopt_policy = ROVPolicy

        # TODO : Review the ROVpp ASes 77 and 78
        # TODO : What does the victim do with subprefix (is it origin)?
        exr_output = [{"asn": 44,
                       "prefix": subprefix_val,
                       "as_path": (44, attacker_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 44,
                       "prefix": prefix_val,
                       "as_path": (44, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 11,
                       "prefix": prefix_val,
                       "as_path": (11, 77, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 77,
                       "prefix": prefix_val,
                       "as_path": (77, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 78,
                       "prefix": prefix_val,
                       "as_path": (44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 12,
                       "prefix": prefix_val,
                       "as_path": (12, 78, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 88,
                       "prefix": prefix_val,
                       "as_path": (88, 86, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": attacker_asn,
                       "prefix": prefix_val,
                       "as_path": (attacker_asn, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": attacker_asn,
                       "prefix": subprefix_val,
                       "as_path": (attacker_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": 86,
                       "prefix": prefix_val,
                       "as_path": (86, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": victim_asn,
                       "prefix": subprefix_val,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": victim_asn,
                       "prefix": prefix_val,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN}]

        run_topology(attack_type, adopt_policy, exr_output)

        
    @pytest.mark.skip(reason="Reynaldo working on it")
    def test_figure_2b(self):
        # TODO : Review the ROVpp ASes 77 and 78
        # TODO : What todo with blackholes?
        exr_output = [{"asn": 44,
                       "prefix": subprefix_val,
                       "as_path": (44, attacker_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 44,
                       "prefix": prefix_val,
                       "as_path": (44, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 11,
                       "prefix": prefix_val,
                       "as_path": (11, 77, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 77,
                       "prefix": prefix_val,
                       "as_path": (77, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 77,
                       "prefix": subprefix_val,
                       "as_path": (77, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS,
                       "blackhole": True},
                      {"asn": 78,
                       "prefix": prefix_val,
                       "as_path": (78, 88, 86, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 12,
                       "prefix": prefix_val,
                       "as_path": (12, 78, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 88,
                       "prefix": prefix_val,
                       "as_path": (88, 86, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": attacker_asn,
                       "prefix": prefix_val,
                       "as_path": (attacker_asn, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": attacker_asn,
                       "prefix": subprefix_val,
                       "as_path": (attacker_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": 86,
                       "prefix": prefix_val,
                       "as_path": (86, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": victim_asn,
                       "prefix": subprefix_val,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": victim_asn,
                       "prefix": prefix_val,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN}]

        run_topology(attack_type=SubprefixHijack().announcements, 
                     adopt_policy=ROVPPV1Policy, 
                     ribs=exr_output)


    @pytest.mark.skip(reason="Reynaldo working on it")
    def test_figure_2b_v1_lite(self):
        # Define the Local Ribs
        exr_output = [{"asn": 44,
                       "prefix": subprefix_val,
                       "as_path": (44, attacker_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 44,
                       "prefix": prefix_val,
                       "as_path": (44, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 11,
                       "prefix": prefix_val,
                       "as_path": (11, 77, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 77,
                       "prefix": prefix_val,
                       "as_path": (77, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 77,
                       "prefix": subprefix_val,
                       "as_path": (77, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS,
                       "blackhole": True},
                      {"asn": 78,
                       "prefix": prefix_val,
                       "as_path": (44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 78,
                       "prefix": prefix_val,
                       "as_path": (44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS,
                       "blackhole": True},
                      {"asn": 12,
                       "prefix": prefix_val,
                       "as_path": (12, 78, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 88,
                       "prefix": prefix_val,
                       "as_path": (88, 86, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": attacker_asn,
                       "prefix": prefix_val,
                       "as_path": (attacker_asn, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": attacker_asn,
                       "prefix": subprefix_val,
                       "as_path": (attacker_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": 86,
                       "prefix": prefix_val,
                       "as_path": (86, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": victim_asn,
                       "prefix": subprefix_val,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": victim_asn,
                       "prefix": prefix_val,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN}]

        run_topology(attack_type=SubprefixHijack().announcements, 
                     adopt_policy=ROVPPV1LitePolicy, 
                     ribs=exr_output)

