#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This file contains system tests for the extrapolator.

For speciifics on each test, see the docstrings under each function.
"""

import pytest

from lib_caida_collector import PeerLink, CustomerProviderLink as CPLink

from .run_example import run_example

from lib_bgp_simulator.enums import ASNs, Prefixes, Timestamps, ROAValidity, Relationships
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


#######################################
# Tests
#######################################

@pytest.mark.skip(reason="Must be converted")
class Test_Subprefix_hijack:

    # TODO : Add v3 to this once implemented
    @pytest.mark.parametrize("adopt_pol",
                              [ROVAS, ROVPPV1Policy, ROVPPV2Policy, ROVPPV2aPolicy])
    def test_blackhole_sending_rules(self, adopt_pol):
        r"""
        TODO: Create code image of scenario (available in google docs "System Tests" slides).
        TODO: create a png of scenario and keep in this directory.
        """

        attack_type = ROVPPSubprefixHijack()

        peer_rows = []
        provider_customer_rows = [[88, 33],
                                  [88, 86],
                                  [33, 12],
                                  [86, victim_asn],
                                  [86, attacker_asn]]
        customer_providers = [CPLink(provider_asn=x[0], customer_asn=x[1]) for x in provider_customer_rows]
        peers = [PeerLink(x[0], x[1]) for x in peer_rows]

        # Set adopting rows
        bgp_ases = [33, 12, attacker_asn, 86, victim_asn]
        adopting_ases = [88]
        as_policies = dict()
        for bgp_as in bgp_ases:
            as_policies[bgp_as] = BGPAS
        for adopting_as in adopting_ases:
            as_policies[adopting_as] = adopt_pol

        ribs = None
        if (adopt_pol == ROVAS):
           ribs = [{'asn': 12, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (12, 33,)},
                   {'asn': 33, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (33, 88,)},
                   {'asn': 86, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (86, victim_asn,)},
                   {'asn': 86, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (86, attacker_asn,)},
                   {'asn': 88, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (88, 86,)},
                   {'asn': victim_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (victim_asn,)},
                   {'asn': victim_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (victim_asn,)},
                   {'asn': attacker_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (attacker_asn, 86,)},
                   {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (attacker_asn,)}] 
    # TODO : Add v3 to this elif when implemented
        elif (adopt_pol == ROVPPV1Policy or 
              adopt_pol == ROVPPV2Policy):
            ribs = [{'asn': 12, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (12, 33,)},
                    {'asn': 33, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (33, 88,)},
                    {'asn': 86, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (86, victim_asn,)},
                    {'asn': 86, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (86, attacker_asn,)},
                    {'asn': 88, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (88, 86,)},
                    {'asn': 88, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (88, 86,), 'blackhole': True},
                    {'asn': victim_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (victim_asn,)},
                    {'asn': victim_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (victim_asn,)},
                    {'asn': attacker_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (attacker_asn, 86,)},
                    {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (attacker_asn,)}]
        elif(adopt_pol == ROVPPV2aPolicy):
            ribs = [{'asn': 12, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (12, 33,)},
                    {'asn': 12, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (12, 33,), 'blackhole': True},
                    {'asn': 33, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (33, 88,)},
                    {'asn': 33, 'origin': victim_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (33, 88,), 'blackhole': True},
                    {'asn': 86, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (86, victim_asn,)},
                    {'asn': 86, 'origin': attacker_asn, 'prefix': subprefix_val, 'recv_relationship': Relationships.CUSTOMERS, 'as_path': (86, attacker_asn,)},
                    {'asn': 88, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (88, 86,)},
                    {'asn': 88, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (88, 86,), 'blackhole': True},
                    {'asn': victim_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (victim_asn,)},
                    {'asn': victim_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (victim_asn,)},
                    {'asn': attacker_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (attacker_asn, 86,)},
                    {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (attacker_asn,)}]
 
        #traceback_dict = None

        #if (adopt_pol == ROVAS):
        #    traceback_dict = {12: Conds.HIJACKED,
        #                      33: Conds.HIJACKED,
        #                      88: Conds.HIJACKED,
        #                      86: Conds.HIJACKED,
        #                      attacker_asn: Conds.HIJACKED,
        #                      victim_asn: Conds.NOTHIJACKED}
        #elif (adopt_pol == ROVPPV1Policy or 
        #      adopt_pol == ROVPPV2aPolicy or
        #      adopt_pol == ROVPPV2Policy or
        #      adopt_pol == ROVASPP_V3):
        #    traceback_dict = {12: Conds.BHOLED,
        #                      33: Conds.BHOLED,
        #                      88: Conds.BHOLED,
        #                      86: Conds.HIJACKED,
        #                      attacker_asn: Conds.HIJACKED,
        #                      victim_asn: Conds.NOTHIJACKED}

        # Create local ribs
        local_ribs = create_local_ribs(ribs)
       
        # Run test checks
        run_example(peers=peers,
                    customer_providers=customer_providers,
                    as_policies=as_policies,
                    announcements=attack_type.announcements,
                    local_ribs=local_ribs,
                    attack_obj=attack_type)


     # TODO : Add v3 to this once implemented
    @pytest.mark.parametrize("adopt_pol",
                              [ROVAS,
                               ROVPPV1Policy,
                               ROVPPV2aPolicy,
                               ROVPPV2Policy])
    def test_relationship_preference(self, adopt_pol):
        r"""
        TODO: Create code image of scenario (available in google docs "System Tests" slides).
        TODO: create a png of scenario and keep in this directory.
        """
        attack_type = ROVPPSubprefixHijack()

        peer_rows = [[77, 11]]
        provider_customer_rows = [[77, 22],
                                  [9, 77],
                                  [9, victim_asn],
                                  [11, 9],
                                  [11, attacker_asn]]
        customer_providers = [CPLink(provider_asn=x[0], customer_asn=x[1]) for x in provider_customer_rows]
        peers = [PeerLink(x[0], x[1]) for x in peer_rows]

        # Set adopting rows
        bgp_ases = [22, 9, victim_asn, 11, attacker_asn]
        adopting_ases = [77]
        as_policies = dict()
        for bgp_as in bgp_ases:
            as_policies[bgp_as] = BGPAS
        for adopting_as in adopting_ases:
            as_policies[adopting_as] = adopt_pol

        ribs = None
        if (adopt_pol == ROVAS):
            ribs = [{'asn': 9, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (9, victim_asn,)},
                    {'asn': 9, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (9, 11,)},
                    {'asn': 11, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (11, 9,)},
                    {'asn': 11, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (11, attacker_asn,)},
                    {'asn': 22, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (22, 77,)},
                    {'asn': 77, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PEERS, 'as_path': (77, 11,)},
                    {'asn': victim_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (victim_asn,)},
                    {'asn': victim_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (victim_asn, 9)},
                    {'asn': attacker_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (attacker_asn, 11,)},
                    {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (attacker_asn,)}]
        elif (adopt_pol == ROVPPV1Policy):
            ribs = [{'asn': 9, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (9, victim_asn,)},
                    {'asn': 9, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (9, 11,)},
                    {'asn': 11, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (11, 9,)},
                    {'asn': 11, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (11, attacker_asn,)},
                    {'asn': 22, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (22, 77,)},
                    {'asn': 77, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PEERS, 'as_path': (77, 11,)},
                    {'asn': 77, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PEERS, 'as_path': (77, 11,), 'blackhole': True},
                    {'asn': victim_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (victim_asn,)},
                    {'asn': victim_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (victim_asn, 9,)},
                    {'asn': attacker_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (attacker_asn, 11,)},
                    {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (attacker_asn,)}] 
        # TODO :  Add v3 when implemented
        elif (adopt_pol == ROVPPV2Policy or
              adopt_pol == ROVPPV2aPolicy):
            ribs = [{'asn': 9, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (9, victim_asn,)},
                    {'asn': 9, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (9, 11,)},
                    {'asn': 11, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (11, 9,)},
                    {'asn': 11, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.CUSTOMERS, 'as_path': (11, attacker_asn,)},
                    {'asn': 22, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (22, 77,)},
                    {'asn': 22, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (22, 77,), 'blackhole': True},
                    {'asn': 77, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PEERS, 'as_path': (77, 11,)},
                    {'asn': 77, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PEERS, 'as_path': (77, 11), 'blackhole': True},
                    {'asn': victim_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (victim_asn,)},
                    {'asn': victim_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (victim_asn, 9,)},
                    {'asn': attacker_asn, 'origin': victim_asn, 'prefix': prefix_val,'recv_relationship': Relationships.PROVIDERS, 'as_path': (attacker_asn, 11,)},
                    {'asn': attacker_asn, 'origin': attacker_asn, 'prefix': subprefix_val,'recv_relationship': Relationships.ORIGIN, 'as_path': (attacker_asn,)}]

        
        #traceback_dict = None
        #if (adopt_pol == ROVAS):
        #    traceback_dict = {22: Conds.HIJACKED,
        #                      77: Conds.HIJACKED,
        #                      11: Conds.HIJACKED,
        #                      9: Conds.HIJACKED,
        #                      victim_asn: Conds.NOTHIJACKED,
        #                      attacker_asn: Conds.HIJACKED}
        ## TODO : Add v3 when implemented
        #elif (adopt_pol == ROVPPV1Policy or 
        #      adopt_pol == ROVPPV2aPolicy or
        #      adopt_pol == ROVPPV2Policy):
        #    traceback_dict = {22: Conds.BHOLED,
        #                      77: Conds.BHOLED,
        #                      11: Conds.HIJACKED,
        #                      9: Conds.HIJACKED,
        #                      victim_asn: Conds.NOTHIJACKED,
        #                      attacker_asn: Conds.HIJACKED}
        
        # Create local ribs
        local_ribs = create_local_ribs(ribs)
       
        # Run test checks
        run_example(peers=peers,
                    customer_providers=customer_providers,
                    as_policies=as_policies,
                    announcements=attack_type.announcements,
                    local_ribs=local_ribs,
                    attack_obj=attack_type)
