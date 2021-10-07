#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains system tests for the extrapolator.

For speciifics on each test, see the docstrings under each function.
"""
import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink

from .run_example import run_example

from lib_bgp_simulator.enums import ASNs, Prefixes, Timestamps, ROAValidity, Relationships
#from lib_bgp_simulator.simulator.attacks import ROVPPSubprefixHijack
from lib_bgp_simulator.engine.bgp_policy import BGPPolicy
from lib_bgp_simulator.engine.bgp_ribs_policy import BGPRIBSPolicy
# from lib_bgp_simulator.announcement import Announcement
from lib_bgp_simulator.engine.rov_policy import ROVPolicy
from ..policies.rovpp_v1_lite_policy import ROVPPV1LitePolicy
from ..policies.rovpp_v1_policy import ROVPPV1Policy
from ..attacks.rovpp_ann import ROVPPAnn
from ..attacks import ROVPPSubprefixHijack
from .utils import create_local_ribs

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
                local_ribs=local_ribs,
                attack_obj=ROVPPSubprefixHijack())


#######################################
# Tests
#######################################


class Test_Figure_2:
    """Tests all example graphs within our paper."""

    def test_figure_2a(self):
        
        # Define Attack type and adoption policy
        attack_type = ROVPPSubprefixHijack().announcements
        adopt_policy = ROVPolicy

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
                       "as_path": (78, 44, victim_asn),
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
                       "as_path": (victim_asn, 44, attacker_asn),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": victim_asn,
                       "prefix": prefix_val,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN}]

        run_topology(attack_type, adopt_policy, exr_output)

    @pytest.mark.skip
    def test_figure_2b(self):
        # TODO : Why ROVpp ASes drop themselves from the path with the subprefix?
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
                       "as_path": (44, attacker_asn),
                       "recv_relationship": Relationships.PROVIDERS,
                       "blackhole": True},
                      {"asn": 78,
                       "prefix": prefix_val,
                       "as_path": (78, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 78,
                       "prefix": subprefix_val,
                       "as_path": (78, 88, 86, victim_asn) ,
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 12,
                       "prefix": prefix_val,
                       "as_path": (12, 78, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 12,
                       "prefix": subprefix_val,
                       "as_path": (12, 78, 88, 86, victim_asn),
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
                       "as_path": (victim_asn, 44, attacker_asn),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": victim_asn,
                       "prefix": prefix_val,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN}]

        run_topology(attack_type=ROVPPSubprefixHijack().announcements, 
                     adopt_policy=ROVPPV1Policy, 
                     ribs=exr_output)

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
                       "as_path": (44, attacker_asn),
                       "recv_relationship": Relationships.PROVIDERS,
                       "blackhole": True},
                      {"asn": 78,
                       "prefix": prefix_val,
                       "as_path": (78, 44, victim_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 78,
                       "prefix": subprefix_val,
                       "as_path": (44, attacker_asn),
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
                       "as_path": (victim_asn, 44, attacker_asn),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": victim_asn,
                       "prefix": prefix_val,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN}]

        run_topology(attack_type=ROVPPSubprefixHijack().announcements, 
                     adopt_policy=ROVPPV1LitePolicy, 
                     ribs=exr_output)

