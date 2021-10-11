from copy import deepcopy
from collections import defaultdict

from ipaddress import ip_network

from lib_bgp_simulator import ROAValidity, Relationships

def _new_ann_better(self,
                    current_ann,
                    current_processed,
                    default_current_recv_rel,
                    new_ann,
                    new_processed,
                    default_new_recv_rel):
    """Assigns the priority to an announcement according to Gao Rexford

    NOTE: processed is processed for second ann"""

    new_rel_better = self._new_rel_better(current_ann,
                                          current_processed,
                                          default_current_recv_rel,
                                          new_ann,
                                          new_processed,
                                          default_new_recv_rel)
    if new_rel_better is not None:
        return new_rel_better
    else:
        new_holes_smaller = self._new_holes_smaller(current_ann, new_ann)
        if new_holes_smaller is not None:
            return new_holes_smaller
        else:
            return self._new_as_path_ties_better(current_ann,
                                                 current_processed,
                                                 new_ann,
                                                 new_processed)


def _new_holes_smaller(self, current_ann, new_ann):
    """Best by hole size"""

    # Holes aren't counted for this prefix
    if current_ann.temp_holes is None:
        return None

    if len(current_ann.temp_holes) > len(new_ann.temp_holes):
        return True
    elif len(current_ann.temp_holes) < len(new_ann.temp_holes):
        return False
    else:
        return None
