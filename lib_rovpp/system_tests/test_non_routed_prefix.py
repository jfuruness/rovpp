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
from ..policies.rovpp_v3_policy import ROVPPV3Policy
from ..attacks.rovpp_ann import ROVPPAnn
from ..attacks import ROVPPSubprefixHijack, ROVPPNonRoutedPrefixHijack, ROVPPSuperprefixPrefixHijack, ROVPPNonRoutedSuperprefixHijack
from .utils import create_local_ribs


__author__ = "Justin Furuness"
__credits__ = ["Justin Furuness"]
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


#######################################
# Helper Functions
#######################################


def run_topology(attack_type, adopt_policy, ribs, hijack_outcomes):
    r"""
          44
        /   \
       77    attacker_asn
      /      
     11      
    """

    peer_rows = []
    provider_customer_rows = [[44, 77],
                              [44, attacker_asn],
                              [77, 11]]
    customer_providers = [CPLink(provider_asn=x[0], customer_asn=x[1]) for x in provider_customer_rows]
    peers = [PeerLink(x[0], x[1]) for x in peer_rows]

    # Set adopting rows
    bgp_ases = [44, 11, attacker_asn]
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

    @pytest.mark.skip(reason="needs outcomes or local_ribs need to be created")
    def test_non_routed_prefix_rov(self):
        attack_type = ROVPPNonRoutedPrefixHijack()
        exr_output = None
        
        hijack_outcomes = {44:Conds.HIJACKED,
                           attacker_asn:Conds.HIJACKED}

        run_topology(attack_type, adopt_policy, exr_output, hijack_outcomes)


    @pytest.mark.skip(reason="needs outcomes or local_ribs need to be created")
    @pytest.mark.parametrize("adopt_pol", [ROVPPV1Policy, ROVPPV2Policy, ROVPPV2aPolicy])
    def test_non_routed_prefix_rovpp(self, adopt_pol):
        attack_type = ROVPPNonRoutedPrefixHijack()
        exr_output = None

        if (adopt_pol == rovppv1policy):
            hijack_outcomes = {44:Conds.HIJACKED,
                               attacker_asn:Conds.HIJACKED}
        elif (adopt_pol == ROVPPV2Policy or
              adopt_pol == ROVPPV2aPolicy):
            hijack_outcomes = {11:Conds.BHOLED,
                               44:Conds.HIJACKED,
                               77:Conds.BHOLED,
                               attacker_asn:Conds.HIJACKED}
         
        run_topology(attack_type, adopt_pol, exr_output, hijack_outcomes)
