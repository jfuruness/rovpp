from lib_bgp_simulator import BGPAS, Prefixes, ROAValidity, Relationships

from .v2 import ROVPPV2SimpleAS
from ..engine_input import ROVPPSubprefixHijack

class ROVPPV3AS(BGPAS, ROVPPV2SimpleAS):
    """If a customer announces a valid route, don't send preventive

        If you send a preventive, must add attacker on route flag to the valid route
            If later the attack is withdrawn, must withdraw this preventive
        Only send preventives to customers
        Anns with attacker on route flag are not allowed to be chosen as safe routes
    """

    name = "ROV++V3"

    __slots__ = tuple()

    def _policy_propagate(self, neighbor, ann, propagate_to, send_rels):
        """Special cases for propagation handled by the V3 policy

        Blackholes propagate normally
        preventives must:
            Only be sent to customers
            Don't send if there was a valid route from that neighbor
        """

        if ann.blackhole:
            return True
            #print("Is this calling the correct process_outgoing_ann_funcs?????")
            return ROVPPV2SimpleAS._policy_propagate(self, neighbor, ann, propagate_to, send_rels)
        # NOTE that preventive is the subprefix. The valid route isn't considered preventive
        elif ann.preventive:
            # Same logic as V2. Don't override because V2 uses this lol
            if self._send_competing_hijack_allowed(ann, propagate_to):
                #input("\n" * 3 + "allowed to be sent" + "\n" * 3)
                # Make sure you don't send to a neighbor that sent a valid route
                # NOTE: that includes neighbors that sent valid route and subprefix
                # imo these two if statements make this policy almost never occur
                safe_route_prefix = Prefixes.PREFIX.value
                if not self._neighbor_sent_valid_ann(neighbor, safe_route_prefix):
                    self._process_outgoing_ann(neighbor, ann, propagate_to, send_rels)
                #else:
                #    # Send that neighbor a blackhole??????????
                #    # On second thought nm, because your sending to customers
                #    # So if customer sent subprefix, you will not replace it (Gao rexford)
            return True
        else:
            return False

    # Ann here is the subprefix since it is a preventive
    def _neighbor_sent_valid_ann(self, neighbor, safe_route_prefix):
        neighbor_info = self._ribs_in.get_unprocessed_ann_recv_rel(neighbor.asn,
                                                                   safe_route_prefix)
        
        return neighbor_info is not None

    def process_incoming_anns(self,
                              recv_relationship,
                              propagation_round=None,
                              engine_input=None,
                              reset_q=True,
                              **kwargs):
        """Process all announcements that were incoming from a specific rel"""

        err = ("This entire policy hardcoded for a victim prefix and attacker subprefix"
               " Not going to make this dynamic because this is a useless policy")
        assert isinstance(engine_input, ROVPPSubprefixHijack), err

        # Holes are invalid subprefixes from the same neighbor
        # We do this here so that we can optimize it
        # Or else it is much too slow to have a generalized version
        # See ROVPP_v1_Lite_slow, it has like 5+ nested for loops

        # Modifies the temp_holes in shallow_anns and returns prefix: blackhole_list dict
        shallow_blackholes = engine_input.count_holes(self)

        BGPAS.process_incoming_anns(self,
                                    recv_relationship,
                                    propagation_round=propagation_round,
                                    engine_input=engine_input,
                                    reset_q=False,
                                    **kwargs)

        if shallow_blackholes:
            self._get_and_assign_preventives(shallow_blackholes, recv_relationship)

            subprefix_ann = self._local_rib.get_ann(Prefixes.SUBPREFIX.value)
            if getattr(subprefix_ann, "preventive", False) is False:
                self._get_and_assign_blackholes(shallow_blackholes, recv_relationship)

        engine_input.remove_temp_holes(self)
        # Move holes from temp_holes and resets q 
        self._reset_q(reset_q)

    def _get_and_assign_preventives(self, shallow_blackholes, recv_relationship):
        """
        Conditions to create a preventive:
            Check the prefix in the local rib. If it has no holes, and no attacker on route flag, this is a safe route

        When creating preventives:
            Modify valid route in your local rib to have attacker on route flag
            Create a subprefix that is a copy of the valid ann but with subprefix
                NOTE: also must make roa validity invalid!!
        """

        unprocessed_invalid_subprefix_anns = list(shallow_blackholes.values())[0]

        # Check if we have a safe alternate (no holes, not attacker on route)
        victim_ann = self._local_rib.get_ann(Prefixes.PREFIX.value)

        # Attacker is on the route
        if (victim_ann is not None
            and ((getattr(victim_ann, "temp_holes") is not None and (len(getattr(victim_ann, "temp_holes", [])) > 0))
                 or((getattr(victim_ann, "holes") is not None and len(getattr(victim_ann, "holes", [])) > 0)))):
            victim_ann.attacker_on_route = True



        # Safe route conditions
        if (victim_ann is not None
            and (victim_ann.temp_holes is None or len(victim_ann.temp_holes) == 0)
            and (victim_ann.holes is None or len(getattr(victim_ann, "holes", [])) == 0)
            and victim_ann.attacker_on_route is False):

            ########
            # In v2, if we recieve hijacks from peers/providers, and a valid route,
            # We connect to the valid route and do nothing
            # In V3 however, we send preventives when v2 would do nothing
            # This causes a problem when V3 has a hidden blackhole
            # In v2, when this occurs, valid ann would have a good chance of competing and winning
            # In v3 however, we subprefix hijack it, making preventives beat valid announcements
            # But because it is a hidden blackhole it routes back to another V3 and gets dropped
            #Jk, this must not have had the attacker on route flag for victim

            # Must do this here, since we don't want to create preventives we won't send
            # Because we should instead create blackholes for that case
            if self._recv_hijack_from_peer_provider(unprocessed_invalid_subprefix_anns):
                # This covers the case when victim_ann has no holes
                # But we are sending a preventive
                victim_ann.attacker_on_route = True
                # TODO Create the preventive ann and store that in local rib
                preventive_ann = victim_ann.copy(prefix=Prefixes.SUBPREFIX.value,
                                                 roa_validity=ROAValidity.INVALID,
                                                 preventive=True)

                self._local_rib.add_ann(preventive_ann)

    def _recv_hijack_from_peer_provider(self, unprocessed_invalid_subprefix_anns):
        # Must check that we got a hijack from a peer/provider
        for unprocessed_ann in unprocessed_invalid_subprefix_anns:
            ann_info = self._ribs_in.get_unprocessed_ann_recv_rel(unprocessed_ann.as_path[0],
                                                                  unprocessed_ann.prefix)
            if ann_info.recv_relationship in [Relationships.PEERS, Relationships.PROVIDERS]:
                return True

        return False
