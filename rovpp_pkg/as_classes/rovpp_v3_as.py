from bgp_simulator_pkg import BGPAS, Prefixes, Relationships, ROVAS
from bgp_simulator_pkg import Scenario, SubprefixHijack

from .non_lite import NonLite
from .v2 import ROVPPV2SimpleAS
from .v1 import ROVPPV1LiteSimpleAS


# Hard coding this because screw it
# This is not how I normally code I assure you
class ROVNoDropPrev(NonLite, BGPAS):
    name = "ROV that deals with preventives"

    def _valid_ann(self, ann, *args, **kwargs) -> bool:
        if ann.invalid_by_roa and not ann.preventive:
            return False
        else:
            return bool(BGPAS._valid_ann(self, ann, *args, **kwargs))

    def _copy_and_process(self,
                          ann,
                          recv_relationship,
                          overwrite_default_kwargs=None):
        """Deep copies ann and modifies attrs"""

        if overwrite_default_kwargs:
            overwrite_default_kwargs["holes"] = self.temp_holes[ann]
        else:
            overwrite_default_kwargs = {"holes": self.temp_holes[ann]}

        return super(ROVPPV1LiteSimpleAS,
                     self)._copy_and_process(  # type: ignore
            ann,
            recv_relationship,
            overwrite_default_kwargs=overwrite_default_kwargs)


class ROVPPV3AS(ROVAS, ROVPPV2SimpleAS):
    """If a customer announces a valid route, don't send preventive

        If you send a preventive,
                must add attacker on route flag to the valid route
            If later the attack is withdrawn, must withdraw this preventive
        Only send preventives to customers
        Anns with attacker on route flag are
            not allowed to be chosen as safe routes
    """

    name = "ROV++V3"

    __slots__ = ()

    def _policy_propagate(self, neighbor, ann, propagate_to, send_rels):
        """Special cases for propagation handled by the V3 policy

        Blackholes propagate normally
        preventives must:
            Only be sent to customers
            Don't send if there was a valid route from that neighbor
        """

        if ann.blackhole:
            # For now do V1
            # return True
            # Is this calling the proper func??
            return ROVPPV2SimpleAS._policy_propagate(self,
                                                     neighbor,
                                                     ann,
                                                     propagate_to,
                                                     send_rels)
        # NOTE that preventive is the subprefix.
        #    The valid route isn't considered preventive
        elif ann.preventive:
            # Same logic as V2. Don't override because V2 uses this lol
            if self._send_competing_hijack_allowed(ann, propagate_to):
                # input("\n" * 3 + "allowed to be sent" + "\n" * 3)
                # Make sure you don't send to a neighbor
                # that sent a valid route
                # NOTE: that includes neighbors
                # that sent valid route and subprefix
                # imo these two if statements
                # make this policy almost never occur
                safe_route_prefix = Prefixes.PREFIX.value
                if not self._neighbor_sent_valid_ann(neighbor,
                                                     safe_route_prefix):
                    return False
                    # self._process_outgoing_ann(neighbor,
                    #                           ann,
                    #                            propagate_to,
                    #                           send_rels)
                # else:
                #    # Send that neighbor a blackhole??????????
                #    # On second thought nm, because your sending to customers
                #    # So if customer sent subprefix,
                #    # you will not replace it (Gao rexford)
            return True
        else:
            return False

    # Ann here is the subprefix since it is a preventive
    def _neighbor_sent_valid_ann(self, neighbor, safe_route_prefix):
        neighbor_info = self._ribs_in.get_unprocessed_ann_recv_rel(
            neighbor.asn, safe_route_prefix)

        return neighbor_info is not None

    def process_incoming_anns(self,
                              *,
                              from_rel: Relationships,
                              propagation_round: int,
                              scenario: "Scenario",
                              reset_q: bool = True):
        """Process all announcements that were incoming from a specific rel"""

        err = ("This entire policy hardcoded for a victim prefix "
               "and attacker subprefix"
               " Not going to make this dynamic "
               "because this is a useless policy")
        assert isinstance(scenario, SubprefixHijack), err

        # Holes are invalid subprefixes from the same neighbor
        # We do this here so that we can optimize it
        # Or else it is much too slow to have a generalized version
        # See ROVPP_v1_Lite_slow, it has like 5+ nested for loops

        self.temp_holes = self._get_ann_to_holes_dict(scenario)

        ROVNoDropPrev.process_incoming_anns(
            self,
            from_rel=from_rel,
            propagation_round=propagation_round,
            scenario=scenario,
            reset_q=False)
        self._get_and_assign_preventives(self.temp_holes, from_rel)

        self._add_blackholes(self.temp_holes, from_rel, scenario)

        # Move holes from temp_holes and resets q
        self._reset_q(reset_q)

    def _reset_q(self, reset_q: bool):
        if reset_q:
            self.temp_holes = dict()
        super(ROVPPV1LiteSimpleAS, self)._reset_q(reset_q)

    def _get_and_assign_preventives(self, holes, recv_relationship):
        """
        Conditions to create a preventive:
            Check the prefix in the local rib.
                If it has no holes, and no attacker on route flag,
                    this is a safe route

        When creating preventives:
            Modify valid route in your local rib to have attacker on route flag
            Create a subprefix that is a copy of the valid ann
                but with subprefix
                NOTE: also must make roa validity invalid!!
        """

        # Check if we have a safe alternate (no holes, not attacker on route)
        victim_ann = self._local_rib.get_ann(Prefixes.PREFIX.value)

        # Attacker is on the route
        if victim_ann is not None and len(victim_ann.holes) > 0:
            self._local_rib.add_ann(victim_ann.copy(
                overwrite_default_kwargs={"attacker_on_route": True}))
        # Safe route - ths condition plus not the two conditions above
        elif victim_ann is not None and victim_ann.attacker_on_route is False:
            # Must do this here, since we don't want to create
            # preventives we won't send
            # Because we should instead create blackholes for that case
            if self._recv_hijack_from_peer_provider():
                # TODO Create the preventive ann and store that in local rib
                preventive_ann = victim_ann.copy(
                    overwrite_default_kwargs={
                        'prefix': Prefixes.SUBPREFIX.value,
                        'roa_valid_length': False,
                        'preventive': True,
                        # This covers the case when victim_ann has no holes
                        # But we are sending a preventivei
                        # ?????????????????????????????????????????????????
                        # Do we need this line?????????????????????????????
                        'attacker_on_route': True,
                        'holes': tuple()})

                self._local_rib.add_ann(preventive_ann)

    def _recv_hijack_from_peer_provider(self):
        """Did we recieve a hijack at any point from a peer or provider??"""

        for ann_info in self._ribs_in.get_ann_infos(Prefixes.SUBPREFIX.value):
            if (ann_info.recv_relationship in [Relationships.PEERS,
                                               Relationships.PROVIDERS]
                and ann_info.unprocessed_ann.invalid_by_roa
                    and not ann_info.unprocessed_ann.preventive):
                return True

        return False

    def _valid_ann(self, ann, *args, **kwargs) -> bool:
        if ann.invalid_by_roa and not ann.preventive:
            return False
        else:
            return bool(BGPAS._valid_ann(self, ann, *args, **kwargs))

    def _copy_and_process(self,
                          ann,
                          recv_relationship,
                          overwrite_default_kwargs=None):
        """Deep copies ann and modifies attrs"""

        if overwrite_default_kwargs:
            overwrite_default_kwargs["holes"] = self.temp_holes[ann]
        else:
            overwrite_default_kwargs = {"holes": self.temp_holes[ann]}

        return super(ROVPPV1LiteSimpleAS, self)._copy_and_process(
            ann,
            recv_relationship,
            overwrite_default_kwargs=overwrite_default_kwargs)
