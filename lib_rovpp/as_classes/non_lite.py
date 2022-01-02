from typing import Optional

from lib_bgp_simulator import Announcement as Ann
from lib_bgp_simulator import BGPSimpleAS
from lib_bgp_simulator import Relationships


class NonLite:
    """Do nothing for new holes better funcs (Lite)"""

    __slots__ = tuple()

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
                    return BGPSimpleAS._new_ann_better(self,
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
