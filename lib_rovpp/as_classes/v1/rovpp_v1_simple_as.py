from typing import Dict, Optional, Tuple

from lib_bgp_simulator import Announcement as Ann
from lib_bgp_simulator import BGPSimpleAS
from lib_bgp_simulator import EngineInput
from lib_bgp_simulator import Relationships

class ROVPPV1SimpleAS(BGPSimpleAS):

    name = "ROV++V1 Simple"

    __slots__ = tuple()

    def _policy_propagate(self, _, ann, *args):
        """Only propagate announcements that aren't blackholes"""

        # Policy handled this ann for propagation (and did nothing)
        return ann.blackhole

    def _new_ann_better(self,
                        current_ann: Optional[Ann],
                        current_processed: bool,
                        default_current_recv_rel: Relationships,
                        new_ann: Ann,
                        new_processed: Relationships,
                        default_new_recv_rel: Relationships,
                        # NOTE: this is set to holes dict
                        holes=None) -> Optional[bool]:
        """Must include this here since we blackhole prefixes now

        This does the same thing as the original func
        except it deprefers blackholes and invalid anns
        """

        if current_ann is None:
            assert new_ann is not None
            return True
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
                return new_blackhole_state_better
            else:
                new_holes_better = self._new_holes_better(
                    current_ann,
                    current_processed,
                    new_ann,
                    new_processed,
                    holes)
                if new_holes_better is not None:
                    return new_holes_better
                else:
                    return super(ROVPPV1SimpleAS, self)._new_ann_better(
                        current_ann,
                        current_processed,
                        default_current_recv_rel,
                        new_ann,
                        new_processed,
                        default_new_recv_rel)

    def _new_validity_better(self, current_ann, new_ann):
        """Returns True if new better, False if old better, None if eq"""

        if not new_ann.invalid_by_roa and current_ann.invalid_by_roa:
            return True
        elif new_ann.invalid_by_roa and not current_ann.invalid_by_roa:
            return False
        else:
            return None

    def _new_blackhole_state_better(self, current_ann, new_ann):
        """Returns True if new better, False if old better, None if eq"""

        if not new_ann.blackhole and current_ann.blackhole:
            return True
        elif new_ann.blackhole and not current_ann.blackhole:
            return False
        else:
            return None

    def _new_holes_better(self,
                          current_ann,
                          current_ann_processed,
                          new_ann,
                          new_ann_processed,
                          holes):
        """Returns new ann has less holes, or None if =="""

        # Could do this using int(processed) but so unreadable

        # Holes for new announcement
        if new_ann_processed:
            new_holes = len(new_ann.holes)
        else:
            new_holes = len(holes[new_ann])

        # Holes for current announcement
        if current_ann_processed:
            current_holes = len(current_ann.holes)
        else:
            current_holes = len(holes[current_ann])

        if new_holes < current_holes:
            return True
        elif new_holes > current_holes:
            return False
        # B explicit for future devs
        # One is not better than the other, return None
        else:
            return None

    def receive_ann(self, ann: Ann, *args, **kwargs):
        """Ensures that announcments are ROV++ and valid"""

        if not hasattr(ann, "blackhole"):
            raise NotImplementedError(
                "Policy can't handle announcements without blackhole attrs")
        return super(ROVPPV1SimpleAS, self).receive_ann(
            ann, *args, **kwargs)

    def process_incoming_anns(self,
                              from_rel: Relationships,
                              *args,
                              propagation_round: Optional[int] = None,
                              engine_input: Optional[EngineInput] = None,
                              reset_q: bool = True,
                              **kwargs):
        """Processes all incoming announcements"""

        holes: Dict[Ann, Tuple[Ann]] = self._get_ann_to_holes_dict(
            engine_input)

        # With this solution, by changing the Gao Rexford, I can actually just
        # process __normally__ and drop nothing, since all invalids are
        # replaced with blackholes in copy and process
        # Must rewrite this to include holes in many different places
        super(ROVPPV1SimpleAS, self).process_incoming_anns(
            from_rel,
            *args,
            propagation_round=propagation_round,
            engine_input=engine_input,
            reset_q=False,
            holes=holes,
            **kwargs)

        self._add_blackholes(from_rel)

        # It's possible that we had a previously valid prefix
        # Then later recieved a subprefix that was invalid
        # So we must recount the holes of each ann in local RIB
        self._recount_holes(propagation_round)

        self._reset_q(reset_q)

    def _recount_holes(self, propagation_round):
        # It's possible that we had a previously valid prefix
        # Then later recieved a subprefix that was invalid
        # Or there was previously an invalid subprefix
        # But later that invalid subprefix was removed
        # So we must recount the holes of each ann in local RIB
        assert propagation_round == 0, "Must recount holes if you plan on this"

    def _get_ann_to_holes_dict(self, engine_input):
        """Gets announcements to a typle of Ann holes

        Holes are subprefix hijacks
        """

        holes = dict()
        for _, ann_list in self._recv_q.prefix_anns():
            for ann in ann_list:
                ann_holes = []
                for subprefix in engine_input.prefix_subprefix_dict[ann.prefix]:
                    for sub_ann_list in self._recv_q.get_ann_list(subprefix):
                        for sub_ann in sub_ann_list:
                            if sub_ann.invalid_by_roa:
                                ann_holes.append(sub_ann)
                holes[ann] = tuple(ann_holes)
        return holes

    def _add_blackholes(self, from_rel):
        """Manipulates local RIB by adding blackholes and dropping invalid"""

        # For each ann in local RIB:
        for _, ann in self._local_rib.prefix_anns():
            # For each hole in ann: (holes are invalid subprefixes)
            for unprocessed_hole_ann in ann.holes:
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
            assert ((ann.blackhole and ann.invalid_by_roa)
                    or not ann.invalid_by_roa)

    def _copy_and_process(self,
                          ann,
                          recv_relationship,
                          holes=None,
                          **extra_kwargs):
        """Deep copies ann and modifies attrs"""

        if ann.invalid_by_roa and not ann.preventive:
            extra_kwargs["blackhole"] = True
            extra_kwargs["traceback_end"] = True
        extra_kwargs["holes"] = holes[ann]
        return super(ROVPPV1SimpleAS, self)._copy_and_process(
            ann, recv_relationship, **extra_kwargs)
