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
from ..attacks import ROVPPSubprefixHijack
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

def run_topology(attack_type, adopt_policy, ribs):
    r"""v3 example with ROV++v2

          /44\\
        53 |  \attacker_asn
       /   |   \
      /    | 87 \
     54    |/  \ \
      \    33   victim_asn
       \  /
        22
    """

    peer_rows = []
    provider_customer_rows = [[44, 53],
                              [44, 33],
                              [44, victim_asn],
                              [44, attacker_asn],
                              [53, 54],
                              [54, 22],
                              [33, 22],
                              [87, 33],
                              [87, victim_asn]]
    customer_providers = [CPLink(provider_asn=x[0], customer_asn=x[1]) for x in provider_customer_rows]
    peers = [PeerLink(x[0], x[1]) for x in peer_rows]

    # Set adopting rows
    bgp_ases = [54, 53, 22, 44, 87, victim_asn, attacker_asn]
    adopting_ases = [33]
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
                attack_obj=attack_type)


#######################################
# Tests
#######################################




class Test_Figure_4:
    """Tests all example graphs within our paper."""

    def test_figure_4a(self):
        # Define Attack type and adoption policy
        attack_type = ROVPPSubprefixHijack()
        adopt_policy = ROVPPV2Policy

        exr_output = [{"asn": 44,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (44, victim_asn,),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 44,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (44, attacker_asn,),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": attacker_asn,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (attacker_asn, 44,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": attacker_asn,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (attacker_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": 53,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (53, 44,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 53,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (53, 44,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 54,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (54, 53,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 54,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (54, 53,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 22,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (22, 33,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 22,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (22, 54,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 87,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (87, victim_asn,),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 33,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (33, 87,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": victim_asn,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": victim_asn,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (victim_asn, 44, attacker_asn,),
                       "recv_relationship": Relationships.PROVIDERS},
		     ]
        run_topology(attack_type, adopt_policy, exr_output)


    @pytest.mark.xfail(reason="Ready for v3 testing once v3 is ready")        
    def test_figure_4b(self):
        # Define Attack type and adoption policy
        attack_type = ROVPPSubprefixHijack()
        adopt_policy = ROVPPV3Policy

        exr_output = [{"asn": 44,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (44, victim_asn,),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 44,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (44, attacker_asn,),
                       "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": attacker_asn,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (attacker_asn, 44,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": attacker_asn,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (attacker_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": 53,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (53, 44,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 53,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (53, 44,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 54,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (54, 53,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 54,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (54, 53,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 22,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (22, 33,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 22,
                       "prefix": subprefix_val,
                       "origin": victim_asn,
                       "as_path": (22, 33,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 87,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (87, victim_asn,),
                        "recv_relationship": Relationships.CUSTOMERS},
                      {"asn": 33,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (33, 87,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": 33,
                       "prefix": subprefix_val,
                       "origin": victim_asn,
                       "as_path": (33, 87,),
                       "recv_relationship": Relationships.PROVIDERS},
                      {"asn": victim_asn,
                       "prefix": prefix_val,
                       "origin": victim_asn,
                       "as_path": (victim_asn,),
                       "recv_relationship": Relationships.ORIGIN},
                      {"asn": victim_asn,
                       "prefix": subprefix_val,
                       "origin": attacker_asn,
                       "as_path": (victim_asn, 44, attacker_asn,),
                       "recv_relationship": Relationships.PROVIDERS},
		     ]

        run_topology(attack_type, adopt_policy, exr_output)
