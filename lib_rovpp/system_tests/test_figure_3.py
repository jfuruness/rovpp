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
from lib_bgp_simulator.engine.bgp_policy import BGPPolicy
from lib_bgp_simulator.engine.bgp_ribs_policy import BGPRIBSPolicy
from lib_bgp_simulator.engine.rov_policy import ROVPolicy
from ..policies.rovpp_v1_lite_policy import ROVPPV1LitePolicy
from ..policies.rovpp_v2_lite_policy import ROVPPV2LitePolicy
from ..policies.rovpp_v2a_lite_policy import ROVPPV2aLitePolicy
from ..policies.rovpp_v1_policy import ROVPPV1Policy
from ..policies.rovpp_v2_policy import ROVPPV2Policy
from ..policies.rovpp_v2a_policy import ROVPPV2aPolicy
from ..attacks.rovpp_ann import ROVPPAnn
from ..attacks import ROVPPSubprefixHijack
from .utils import create_local_ribs

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

#######################################
# Helper Functions
#######################################

def run_topology(attack_type, rov_adopting_ases, rovpp_adopt_policy, rovpp_adopting_ases, ribs):
    r"""v2 example with ROV++V1 and ROV

              /44\
             / / \\attacker_asn
            /  54 \ 
           /  /    56
          77  55    \
           | /       victim_asn
          11    
          / \
         32 33  
        """

    # Define Graph data
    peer_rows = []
    provider_customer_rows = [[44, 77],
                              [44, 54],
                              [44, 56],
                              [44, attacker_asn],
                              [77, 11],
                              [11, 32],
                              [11, 33],
                              [54, 55],
                              [55, 11],
                              [56, victim_asn]]
    customer_providers = [CPLink(provider_asn=x[0], customer_asn=x[1]) for x in provider_customer_rows]
    peers = [PeerLink(x[0], x[1]) for x in peer_rows]

    # Set adopting rows
    bgp_ases = [11, 54, 55, 44, attacker_asn, 56, victim_asn]
    as_policies = dict()
    for bgp_as in bgp_ases:
        as_policies[bgp_as] = BGPRIBSPolicy
        print(f"AS: {bgp_as}, Policy: {as_policies[bgp_as]}")
    for rov_adopting_as in rov_adopting_ases:
        as_policies[rov_adopting_as] = ROVPolicy
        print(f"AS: {rov_adopting_as}, Policy: {as_policies[rov_adopting_as]}")
    for adopting_as in rovpp_adopting_ases:
        as_policies[adopting_as] = rovpp_adopt_policy
        print(f"AS: {adopting_as}, Policy: {as_policies[adopting_as]}")

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



class Test_Figure_3:
    """
    Tests all example graphs within our paper.
    """
    @pytest.mark.parametrize("adopt_pol", [ROVPPV1Policy, ROVPPV1LitePolicy])
    def test_figure_3a(self, adopt_pol):
        # Define Attack type and adoption policy
        attack_type = ROVPPSubprefixHijack().announcements
        rov_adopting_ases = [32, 33]
        rovpp_adopt_policy = adopt_pol 
        rovpp_adopting_ases = [77]

        exr_output = [{"asn": 32,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (32, 11),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 33,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (33, 11),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": victim_asn,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": 11,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (11, 77),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 77,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (77, 44),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 55,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (55, 54),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 56,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (56, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 54,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (54, 44),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 44,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (44, 56, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": attacker_asn,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (attacker_asn, 44),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": victim_asn,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (victim_asn, 56, 44, attacker_asn),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 11,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (11, 55),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 55,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (55, 54),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 56,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (56, 44),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 54,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (54, 44),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 44,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (44, attacker_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": attacker_asn,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (attacker_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": 77,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (77, 44),
                       "recv_relationship": Relationships.PROVIDERS,
                       "blackhole": True},
             ]
        run_topology(attack_type, rov_adopting_ases, rovpp_adopt_policy, rovpp_adopting_ases, exr_output)


    # TODO : When v3 is implemented add it to this test.
    @pytest.mark.parametrize("adopt_pol", [ROVPPV2Policy, ROVPPV2aPolicy, ROVPPV2LitePolicy, ROVPPV2aLitePolicy])
    def test_figure_3b(self, adopt_pol):
        # define attack type and adoption policy
        attack_type = ROVPPSubprefixHijack().announcements
        rov_adopting_ases = [32]
        rovpp_adopt_policy = adopt_pol
        rovpp_adopting_ases = [77, 33]
      
        exr_output = [{"asn": 32,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (32, 11),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 33,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (33, 11),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": victim_asn,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": 11,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (11, 77),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 77,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (77, 44),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 55,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (55, 54),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 56,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (56, victim_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 54,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (54, 44),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 44,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (44, 56),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": attacker_asn,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (attacker_asn, 44),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": victim_asn,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 11,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (11, 77),
                       "recv_relationship": Relationships.PROVIDERS,
                       "blackhole": True},
                      {"asn": 55,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (55, 54),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 56,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (56, 44),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 54,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (54, 44),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 44,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (44, attacker_asn),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": attacker_asn,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (attacker_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": 77,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (77, 44),
                       "recv_relationship": Relationships.PROVIDERS,
                       "blackhole": True},
                      # 32 rejects the blackhole announcement as invalid
                      {"asn": 33,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (33, 11),
                       "recv_relationship": Relationships.PROVIDERS,
                       "blackhole": True},
             ]
        run_topology(attack_type, rov_adopting_ases, rovpp_adopt_policy, rovpp_adopting_ases, exr_output)

