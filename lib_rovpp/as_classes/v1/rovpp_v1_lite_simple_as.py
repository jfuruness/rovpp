from copy import deepcopy
from collections import defaultdict
from typing import Dict, Optional

from ipaddress import ip_network

from lib_bgp_simulator import BGPSimpleAS, Relationships

from .rovpp_ann import ROVPPAnn


class ROVPPV1LiteSimpleAS(BGPSimpleAS):

    name = "ROV++V1 Lite Simple"

    __slots__ = tuple()

    def _policy_propagate(self, _, ann, *args):
        """Only propagate announcements that aren't blackholes"""

        # Policy handled this ann for propagation (and did nothing)
        return ann.blackhole

    def _new_ann_better(self,
                        current_ann: Optional[Ann],
                        current_processed: bool,
                        current_hole_count: int,
                        default_current_recv_rel: Relationships,
                        new_ann: Ann,
                        new_processed: Relationships,
                        new_hole_count: int,
                        default_new_recv_rel: Relationships) -> Optional[bool]:
        """Must include this here since we blackhole prefixes now"""

        # Valid > invalid
        new_validity_better = self._new_validity_better(current_ann,
                                                        new_ann)
        if new_validity_better is not None:
            return new_validity_better
        else:
            # Not blackhole > blackhole
            new_blackhole_state_better = self._new_blackhole_state_better(
                current_ann, new_ann)
            if new_blackhole_state_better is not None:
                return new_blackhole_state_better:
            else:
                # NOTE: Add hole counting here for non lite versions
                return super(ROVPPV1LiteSimpleAS, self)._new_ann_better(
                    current_ann,
                    current_processed,
                    default_current_recv_rel,
                    new_ann,
                    new_processed,
                    default_new_recv_rel)

    def receive_ann(self, ann: Ann, *args, **kwargs):
        """Ensures that announcments are ROV++ and valid"""

        if not hasattr(ann, "blackholes"):
            raise NotImplementedError(
                "Policy can't handle announcements without blackhole attrs")
        return super(ROVPPV1LiteSimpleAS, self).receive_ann(
            ann, *args, **kwargs)

    def processing_incoming_ann(self,
                                from_rel: Relationships,
                                *args,
                                propagation_round: Optional[int] = None,
                                engine_input: Optional[EngineInput] = None,
                                reset_q: bool = True,
                                **kwargs):
        """Processes all incoming announcements"""

        holes: Dict[ROVPPAnn, Tuple[ROVPPAnn]] = self._get_ann_to_holes_dict()

        # With this solution, by changing the Gao Rexford, I can actually just
        # process __normally__ and drop nothing
        # Then afterwards, I can go in, and anything that is invalid, I can
        # simply replace with blackholes or drop then
        self.process_incoming_anns(self,
                                   recv_relationship,
                                   *args,
                                   propagation_round=propagation_round,
                                   engine_input=engine_input,
                                   reset_q=False,
                                   **kwargs)

        self._add_blackholes(from_rel, holes)

        self.reset_q(reset_q)

    def _add_blackholes(self, from_rel, holes_dict):
        """Manipulates local RIB by adding blackholes and dropping invalid"""

        # For each ann in local RIB:
        for _, ann in self._local_rib.prefix_anns():
            # For each hole in ann: (holes are invalid subprefixes)
            for unprocessed_hole_ann, rel in holes_dict[ann]:
                # If there is not an existing valid ann for that hole subprefix
                existing_local_rib_subprefix_ann = self._local_rib.get_ann(
                    unprocessed_hole_ann.prefix)

                if (existing_local_rib_subprefix_ann is None
                    or existing_local_rib_subprefix_ann.invalid_by_roa):
                        # Remove current ann and replace with blackhole
                        self._local_rib.remove_ann(unprocessed_hole_ann.prefix)
                        # Create the blackhole
                        blackhole = self._copy_and_process(unprocessed_hole_ann,
                                                           from_rel)
                        # Add the blackhole
                        self._local_rib.add_ann(blackhole)
            # Do nothing - ann should already be a blackhole
            if ann.invalid_by_roa:
                assert ann.blackhole

    def _copy_and_process(self, ann, recv_relationship, **extra_kwargs):
        """Deep copies ann and modifies attrs"""

        if ann.invalid_by_roa and not ann.preventive:
            extra_kwargs[blackhole] = True
        return super(ROVPPV1LiteSimpleAS, self)._copy_and_process(
            ann, recv_relationship, **extra_kwargs)
            


raise NotImplementedError("OLD")

    def process_incoming_anns(self,
                              recv_relationship,
                              propagation_round=None,
                              engine_input=None,
                              reset_q=True,
                              **kwargs):
        """Process all announcements that were incoming from a specific rel"""

        # Holes are invalid subprefixes from the same neighbor
        # We do this here so that we can optimize it
        # Or else it is much too slow to have a generalized version
        # See ROVPP_v1_Lite_slow, it has like 5+ nested for loops

        # Modifies the temp_holes in shallow_anns and returns prefix: blackhole_list dict
        shallow_blackholes = engine_input.count_holes(self)

        super(ROVPPV1LiteSimpleAS, self).process_incoming_anns(recv_relationship,
                                                             propagation_round=propagation_round,
                                                             engine_input=engine_input,
                                                             reset_q=False,
                                                             **kwargs)

        self._get_and_assign_blackholes(shallow_blackholes, recv_relationship)

        engine_input.remove_temp_holes(self)
        # Move holes from temp_holes and resets q
        self._reset_q(reset_q)


##############
# Blackholes #
##############

    def _get_and_assign_blackholes(self, shallow_blackholes_dict, recv_relationship):
        """Gets blackholes and assigns them"""

        # For any announcement we have that has blackholes
        # TODO fix _info

        blackholes = []
        for prefix, ann in self._local_rib.prefix_anns():
            if ann.temp_holes is not None:
                # For every hole/invalid_subprefix
                for invalid_subprefix_ann in ann.temp_holes:
                    #assert isinstance(invalid_subprefix_ann, ROVPPAnn)

                    # Make hole and add to RIB
                    bhole = self._copy_and_process(invalid_subprefix_ann,
                                                   recv_relationship,
                                                   blackhole=True,
                                                   traceback_end=True)
                    blackholes.append(bhole)
        # must be done this way so dict doesn't change size during iteratoin
        for blackhole in blackholes:
            self._local_rib.add_ann(blackhole)
