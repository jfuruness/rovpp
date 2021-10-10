#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains system tests for the extrapolator.

For speciifics on each test, see the docstrings under each function.
"""
import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink

from .run_example import run_example

from lib_bgp_simulator.enums import ASNs, Prefixes, Timestamps, ROAValidity, Relationships
from lib_bgp_simulator.engine import LocalRib
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
from ..attacks import ROVPPSubprefixHijack
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

#######################################
# Tests
#######################################

class Test_Special_Cases:
    """Tests all example graphs within our paper."""

    @pytest.mark.parametrize("adopt_pol", [ROVPPV2Policy, ROVPPV2LitePolicy])
    def test_v2_customer_blackhole(self, adopt_pol):
        r"""
             55
           /    \
         44      3
                /  \
              attacker_asn   victim_asn

        Here we're testing that v2 ASes should not create blackhole announcements for attack
        announcements received from a customer, but rather just drop and blackhole the announcement.
        That can be capture here as 55 and 44 implementing ASes. AS 44 should not have a blackhole, but
        AS 55 should have a blackhole.
        """

        attack_type = ROVPPSubprefixHijack().announcements
        peer_rows = []
        provider_customer_rows = [[55, 44],
                                  [55, 3],
                                  [3, attacker_asn],
                                  [3, victim_asn]]
        customer_providers = [CPLink(provider_asn=x[0], customer_asn=x[1]) for x in provider_customer_rows]
        peers = [PeerLink(x[0], x[1]) for x in peer_rows]

        # Set adopting rows
        bgp_ases = [3, attacker_asn, victim_asn]
        adopting_ases = [55, 44]
        as_policies = dict()
        for bgp_as in bgp_ases:
            as_policies[bgp_as] = BGPAS
        for adopting_as in adopting_ases:
            as_policies[adopting_as] = adopt_pol
        
        exr_output = [
            {'asn': victim_asn, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (victim_asn,), 'recv_relationship': Relationships.ORIGIN},
            {'asn': victim_asn, 'origin': attacker_asn, 'prefix': subprefix_val, 'as_path': (victim_asn, 3, attacker_asn,), 'recv_relationship': Relationships.PROVIDERS},
            {'asn': 44, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (44, 55,), 'recv_relationship': Relationships.PROVIDERS},
            {'asn': 55, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (55, 3,), 'recv_relationship': Relationships.CUSTOMERS},
            {'asn': 55, 'origin': attacker_asn, 'prefix': subprefix_val, 'as_path': (55, 3,), 'recv_relationship': Relationships.CUSTOMERS, 'blackhole': True},
            {'asn': 3, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (3, victim_asn,), 'recv_relationship': Relationships.CUSTOMERS},
            {'asn': 3, 'origin': attacker_asn, 'prefix': subprefix_val, 'as_path': (3, attacker_asn,), 'recv_relationship': Relationships.CUSTOMERS},
            {'asn': attacker_asn, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (attacker_asn, 3,), 'recv_relationship': Relationships.PROVIDERS},
            {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': subprefix_val, 'as_path': (attacker_asn,), 'recv_relationship': Relationships.ORIGIN}
        ]
        # Create local ribs
        local_ribs = create_local_ribs(exr_output)

        # Run test checks
        run_example(peers=peers,
                    customer_providers=customer_providers,
                    as_policies=as_policies,
                    announcements=attack_type,
                    local_ribs=local_ribs,
                    attack_obj=ROVPPSubprefixHijack())


    @pytest.mark.parametrize("adopt_pol", [ROVPPV2Policy, ROVPPV2LitePolicy])
    def test_v2_customer_peer_and_provider(self, adopt_pol):
        r"""
             55 --- 88
           /    \     \
         22      33    44
                /  \
              attacker_asn   victim_asn

        """
        attack_type = ROVPPSubprefixHijack().announcements
        peer_rows = [[55, 88]]
        provider_customer_rows = [[55, 22],
                                  [55, 33],
                                  [33, attacker_asn],
                                  [33, victim_asn],
                                  [88, 44]]
        customer_providers = [CPLink(provider_asn=x[0], customer_asn=x[1]) for x in provider_customer_rows]
        peers = [PeerLink(x[0], x[1]) for x in peer_rows]

        # Set adopting rows
        bgp_ases = [33, 22, 44, attacker_asn, victim_asn, 88]
        adopting_ases = [55]
        as_policies = dict()
        for bgp_as in bgp_ases:
            as_policies[bgp_as] = BGPAS
        for adopting_as in adopting_ases:
            as_policies[adopting_as] = adopt_pol
        
        exr_output = [
            {'asn': attacker_asn, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (attacker_asn, 33,), 'recv_relationship': Relationships.PROVIDERS}, 
            {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': subprefix_val, 'as_path': (attacker_asn,), 'recv_relationship': Relationships.ORIGIN}, 
            {'asn': 44, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (44, 88,), 'recv_relationship': Relationships.PROVIDERS}, 
            {'asn': victim_asn, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (victim_asn,), 'recv_relationship': Relationships.ORIGIN}, 
            {'asn': victim_asn, 'origin': attacker_asn, 'prefix': subprefix_val, 'as_path': (victim_asn, 33,), 'recv_relationship': Relationships.PROVIDERS}, 
            {'asn': 55, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (55, 33,), 'recv_relationship': Relationships.CUSTOMERS}, 
            {'asn': 55, 'origin': attacker_asn, 'prefix': subprefix_val, 'as_path': (55, 33,), 'recv_relationship': Relationships.CUSTOMERS, 'blackhole': True}, 
            {'asn': 22, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (22, 55,), 'recv_relationship': Relationships.PROVIDERS}, 
            {'asn': 88, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (88, 55,), 'recv_relationship': Relationships.PEERS}, 
            {'asn': 33, 'origin': victim_asn, 'prefix': prefix_val, 'as_path': (33, victim_asn,), 'recv_relationship': Relationships.CUSTOMERS}, 
            {'asn': 33, 'origin': attacker_asn, 'prefix': subprefix_val, 'as_path': (33, attacker_asn,), 'recv_relationship': Relationships.CUSTOMERS} 
        ]
        # Create local ribs
        local_ribs = create_local_ribs(exr_output)

        # Run test checks
        run_example(peers=peers,
                    customer_providers=customer_providers,
                    as_policies=as_policies,
                    announcements=attack_type,
                    local_ribs=local_ribs,
                    attack_obj=ROVPPSubprefixHijack())

