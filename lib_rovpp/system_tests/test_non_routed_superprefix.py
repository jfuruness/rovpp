#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains system tests for the extrapolator.

For speciifics on each test, see the docstrings under each function.
"""
import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink

from .run_example import run_example

from lib_bgp_simulator.enums import ASNs, Prefixes, Timestamps, ROAValidity, Relationships
from lib_bgp_simulator import LocalRib
from lib_bgp_simulator import BGPAS
from lib_bgp_simulator import BGPRIBsAS
from lib_bgp_simulator import ROVAS
from ..policies.rovpp_v1_lite_policy import ROVPPV1LitePolicy
from ..policies.rovpp_v2_lite_policy import ROVPPV2LitePolicy
from ..policies.rovpp_v2a_lite_policy import ROVPPV2aLitePolicy
from ..policies.rovpp_v1_policy import ROVPPV1Policy
from ..policies.rovpp_v2_policy import ROVPPV2Policy
from ..policies.rovpp_v2a_policy import ROVPPV2aPolicy
from ..attacks.rovpp_ann import ROVPPAnn
from ..attacks import ROVPPNonRoutedSuperprefixHijack
from .utils import create_local_ribs


__author__ = "Reynaldo Morillo"
__credits__ = ["Reynaldo Morillo"]
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

atk_kwargs = {"prefix": superprefix_val,
              "timestamp": Timestamps.ATTACKER.value,
              "seed_asn": None,
              "roa_validity": ROAValidity.INVALID,
              "withdraw": False,
              "traceback_end": False,
              "holes": None,
              "blackhole": False,
              "temp_holes": None}

atk_prefix_kwargs = {"prefix": prefix_val,
                     "timestamp": Timestamps.ATTACKER.value,
                     "seed_asn": None,
                     "roa_validity": ROAValidity.UNKNOWN,
                     "withdraw": False,
                     "traceback_end": False,
                     "holes": None,
                     "blackhole": False,
                     "temp_holes": None}


#######################################
# Helper Functions
#######################################


def run_topology(attack_type, adopt_policy, ribs, hijack_outcomes):
    r"""non_routed superprefix attack with v1

         44
       /   \
      77    attacker_asn
     /      
    victim_asn      

    superprefix = 1.0.0.0/8
    non_routed_prefix = 1.2.0.0/16
    """
    peer_rows = []
    provider_customer_rows = [[44, 77],
                              [44, attacker_asn],
                              [77, victim_asn]]
    customer_providers = [CPLink(provider_asn=x[0], customer_asn=x[1]) for x in provider_customer_rows]
    peers = [PeerLink(x[0], x[1]) for x in peer_rows]

    # Set adopting rows
    bgp_ases = [44, victim_asn, attacker_asn]
    adopting_ases = [77]
    as_policies = dict()
    for bgp_as in bgp_ases:
        as_policies[bgp_as] = BGPAS
    for adopting_as in adopting_ases:
        as_policies[adopting_as] = adopt_policy
    
    # Create local ribs
    local_ribs = create_local_ribs(ribs)

    # Run test checks
    run_example(peers=peers,
                customer_providers=customer_providers,
                as_policies=as_policies,
                announcements=attack_type.announcements,
                local_ribs=local_ribs,
                outcomes=hijack_outcomes,
                attack_obj=attack_type)

    
#######################################
# Tests
#######################################


class Test_Non_Routed_Superprefix:
    """Tests all example graphs within our paper."""

    def test_non_routed_superprefix_rov(self):
        attack_type = ROVPPNonRoutedSuperprefixHijack()
        adopt_policy = ROVAS

        exr_output = [
            {'asn': victim_asn, 'origin': attacker_asn, 'prefix': superprefix_val, 'as_path':(victim_asn, 77), 'recv_relationship': Relationships.PROVIDERS, 'kwargs': atk_kwargs},
            {'asn': 44, 'origin': attacker_asn, 'prefix': superprefix_val, 'as_path':(44, attacker_asn), 'recv_relationship': Relationships.CUSTOMERS, 'kwargs': atk_kwargs},
            {'asn': 44, 'origin': attacker_asn, 'prefix': prefix_val, 'as_path':(44, attacker_asn), 'recv_relationship': Relationships.CUSTOMERS, 'kwargs': atk_prefix_kwargs},
            {'asn': 77, 'origin': attacker_asn, 'prefix': superprefix_val, 'as_path':(77, 44), 'recv_relationship': Relationships.PROVIDERS, 'kwargs': atk_kwargs},
            {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': superprefix_val, 'as_path':(attacker_asn, ), 'recv_relationship': Relationships.ORIGIN, 'kwargs': atk_kwargs},
            {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': prefix_val, 'as_path':(attacker_asn, ), 'recv_relationship': Relationships.ORIGIN, 'kwargs': atk_prefix_kwargs}
        ]
        
        hijack_outcomes = None
        #hijack_outcomes = {victim_asn:Conds.HIJACKED,
        #                  44:Conds.HIJACKED,
        #                  77:Conds.HIJACKED,
        #                  attacker_asn:Conds.HIJACKED}

        run_topology(attack_type, adopt_policy, exr_output, hijack_outcomes)

    @pytest.mark.skip(reason="Need to create local rib and/or outcomes")
    @pytest.mark.parametrize("adopt_pol", [ROVPPV1Policy, ROVPPV2Policy, ROVPPV2aPolicy]) 
    def test_non_routed_superprefix_rovpp(self, adopt_pol):
        attack_type = ROVPPNonRoutedSuperprefixHijack()

        #exr_output = [
        #         {'asn': victim_asn, 'origin': attacker_asn, 'prefix': superprefix_val, 'as_path':(victim_asn, 77)},
        #         {'asn': 44, 'origin': attacker_asn, 'prefix': superprefix_val, 'as_path':(44, attacker_asn)},
        #         {'asn': 44, 'origin': attacker_asn, 'prefix': prefix_val, 'as_path':(44, attacker_asn)},
        #         {'asn': 77, 'origin': attacker_asn, 'prefix': superprefix_val, 'as_path':(77, 44)},
        #         {'asn': 77, 'prefix': prefix_val, 'origin': 64512, 'as_path':(77, 64512)},
        #         {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': superprefix_val, 'as_path':(attacker_asn, 64513)},
        #         {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': prefix_val, 'as_path':(attacker_asn, 64513)}
        #        ]
        exr_output = None 
        
        hijack_outcomes = None
        #hijack_outcomes = {victim_asn:Conds.BHOLED,
        #                  44:Conds.HIJACKED,
        #                  77:Conds.BHOLED,
        #                  attacker_asn:Conds.HIJACKED}

        run_topology(attack_type, adopt_pol, exr_output, hijack_outcomes)
