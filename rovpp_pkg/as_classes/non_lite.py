from typing import Optional

from bgp_simulator_pkg import Announcement as Ann
from bgp_simulator_pkg import BGPSimpleAS
from bgp_simulator_pkg import Relationships


class NonLite:
    """Do nothing for new holes better funcs (Lite)"""

    def _new_ann_better(self,  # type: ignore
                        current_ann: Optional[Ann],
                        current_processed: bool,
                        default_current_recv_rel: Relationships,
                        new_ann: Ann,
                        new_processed: Relationships,
                        default_new_recv_rel: Relationships,
                        ) -> bool:
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
        # This is a no op without specific subclasses, we can ignore
        # for the purposes of our paper
        if new_validity_better is not None:
            return new_validity_better  # pragma: no cover
        else:
            # Not blackhole > blackhole
            new_blackhole_state_better = self._new_blackhole_state_better(
                current_ann, new_ann)
            # This is a no unless you create a class that considers
            # both blackholes and preventives valid, which we do not
            # So we can ignore for this paper
            if new_blackhole_state_better is not None:
                return new_blackhole_state_better  # pragma: no cover
            else:
                # First check if new relationship is better
                new_rel_better: Optional[bool] = BGPSimpleAS._new_rel_better(
                    self,
                    current_ann,
                    current_processed,
                    default_current_recv_rel,
                    new_ann,
                    new_processed,
                    default_new_recv_rel)
                # If new rel better is True or False, return it
                if new_rel_better is not None:
                    return new_rel_better
                else:
                    new_holes_better = self._new_holes_better(
                                    current_ann,
                                    current_processed,
                                    new_ann,
                                    new_processed)
                    if new_holes_better is not None:
                        return new_holes_better
                    else:
                        # Return the outcome of as path and tiebreaks
                        # mypy doesn't recognize that this is always a bool
                        return BGPSimpleAS._new_as_path_ties_better(
                            self,
                            current_ann,  # type: ignore
                            current_processed,
                            new_ann,
                            new_processed)

    def _new_validity_better(self,
                             current_ann,
                             new_ann
                             ) -> Optional[bool]:
        """Returns True if new better, False if old better, None if eq"""

        if not new_ann.invalid_by_roa and current_ann.invalid_by_roa:
            # This only occurs in subclasses we do not implement
            # so we will ignore it to save time
            return True  # pragma: no cover
        elif new_ann.invalid_by_roa and not current_ann.invalid_by_roa:
            # This only occurs in subclasses we do not implement
            # so we will ignore it to save time
            return False  # pragma: no cover
        else:
            return None

    def _new_blackhole_state_better(self,
                                    current_ann,
                                    new_ann
                                    ) -> Optional[bool]:
        """Returns True if new better, False if old better, None if eq

        This function is basically a no op unless you create a subclass
        that doesn't drop invalid announcements for some reason and also
        keeps preventives and blackholes. To save time for this research
        paper, we omit the coverage
        """

        if not new_ann.blackhole and current_ann.blackhole:
            return True  # pragma: no cover
        elif new_ann.blackhole and not current_ann.blackhole:
            return False  # pragma: no cover
        # Preventives > blackholes
        elif new_ann.preventive and current_ann.blackhole:
            return True  # pragma: no cover
        else:
            return None

    def _new_holes_better(self,
                          current_ann,
                          current_ann_processed,
                          new_ann,
                          new_ann_processed
                          ) -> Optional[bool]:
        """Returns new ann has less holes, or None if =="""

        # Could do this using int(processed) but so unreadable

        # Holes for new announcement
        if new_ann_processed:
            # This only occurs in subclasses we do not implement
            # so we will ignore it to save time
            new_holes = len(new_ann.holes)  # pragma: no cover
        else:
            new_holes = len(self.temp_holes[new_ann])  # type: ignore

        # Holes for current announcement
        if current_ann_processed:
            # This only occurs in subclasses we do not implement
            # so we ill ignore it to save time
            current_holes = len(current_ann.holes)  # pragma: no cover
        else:
            current_holes = len(self.temp_holes[current_ann])  # type: ignore

        if new_holes < current_holes:
            return True
        elif new_holes > current_holes:
            return False
        # B explicit for future devs
        # One is not better than the other, return None
        else:
            return None
