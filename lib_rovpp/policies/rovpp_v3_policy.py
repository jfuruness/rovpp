from lib_bgp_simulator import BGPRIBsAS, Prefixes

from .rovpp_v2_policy import ROVPPV2Policy

class ROVPPV3Policy(BGPRIBsAS, ROVPPV2Policy):
    """If a customer announces a valid route, don't send preventive

        If you send a preventive, must add attacker on route flag to the valid route
            If later the attack is withdrawn, must withdraw this preventive
        Only send preventives to customers
        Anns with attacker on route flag are not allowed to be chosen as safe routes
    """

    name = "ROV++V3"

    __slots__ = []

    def _policy_propagate(self, neighbor, ann, propagate_to, send_rels):
        """Special cases for propagation handled by the V3 policy

        Blackholes propagate normally
        preventives must:
            Only be sent to customers
            Don't send if there was a valid route from that neighbor
        """

        if ann.blackhole:
            return ROVPPV2Policy._policy_propagate(self, *args, **kwargs)
        # NOTE that preventive is the subprefix. The valid route isn't considered preventive
        elif ann.preventive:
            # Same logic as V2. Don't override because V2 uses this lol
            if _send_competing_hijack_allowed(ann, propagate_to):
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
        return neighbor_info is None

    def process_incoming_anns(self,
                              recv_relationship,
                              propagation_round=None,
                              engine_input=None,
                              reset_q=True,
                              **kwargs):
        """Process all announcements that were incoming from a specific rel"""

        err = ("This entire policy hardcoded for a victim prefix and attacker subprefix"
               " Not going to make this dynamic because this is a useless policy")
        assert isinstance(engine_input, SubprefixHijack), err

        # Holes are invalid subprefixes from the same neighbor
        # We do this here so that we can optimize it
        # Or else it is much too slow to have a generalized version
        # See ROVPP_v1_Lite_slow, it has like 5+ nested for loops

        # Modifies the temp_holes in shallow_anns and returns prefix: blackhole_list dict
        shallow_blackholes = engine_input.count_holes(self)

        BGPRIBsAS.process_incoming_anns(self,
                                        recv_relationship,
                                        propagation_round=propagation_round,
                                        engine_input=engine_input,
                                        reset_q=False,
                                        **kwargs)

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

        # Safe route conditions
        if (victim_ann is not None
            and len(victim_ann.temp_holes) == 0
            and victim_ann.attacker_on_route == False):

            # Must do this here, since we don't want to create preventives we won't send
            # Because we should instead create blackholes for that case
            if self._recv_hijack_from_peer_provider(unprocessed_invalid_subprefix_anns):
                # TODO Change the local rib ann to have attacker on route flag
                victim_ann.attacker_on_route = True
                # TODO Create the preventive ann and store that in local rib
                preventive_ann = victim_ann.copy(prefix=Prefixes.SUBPREFIX.value,
                                                 roa_validity=ROAValidity.INVALID,
                                                 preventive=True)

                self._local_rib.add_ann(preventive_ann.prefix, preventive_ann)

    def _recv_hijack_from_peer_provider(self, unprocessed_invalid_subprefix_anns):
        # Must check that we got a hijack from a peer/provider
        for unprocessed_ann in unprocessed_invalid_subprefix_anns:
            _, subprefix_recv_rel = self._ribs_in.get_unprocessed_ann(unprocessed_ann.as_path[0],
                                                                      unprocessed_ann.prefix)
            if subprefix_recv_rel in [Relationships.PEERS, Relationships.PROVIDERS]:
                return True

        return False
