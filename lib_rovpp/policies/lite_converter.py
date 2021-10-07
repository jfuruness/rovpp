from copy import deepcopy
from collections import defaultdict

from ipaddress import ip_network

from lib_bgp_simulator import BGPPolicy, ROAValidity, ROVPolicy, Relationships

def _new_ann_is_better(policy_self,
                       self,
                       current_best_ann,
                       current_best_ann_processed,
                       new_ann,
                       new_ann_processed,
                       recv_relationship: Relationships):
    """Assigns the priority to an announcement according to Gao Rexford

    NOTE: processed is processed for second ann"""

    assert self.asn not in new_ann.as_path, "Should have been removed in ann validation func"

    new_rel_is_better = policy_self._new_relationship_is_better(current_best_ann,
                                                                current_best_ann_processed,
                                                                new_ann,
                                                                new_ann_processed,
                                                                recv_relationship)
    if new_rel_is_better is not None:
        return new_rel_is_better
    else:
        best_by_hole_size = policy_self._new_hole_size_is_smaller(current_best_ann, new_ann)
        if best_by_hole_size is not None:
            return best_by_hole_size
        else:
            return policy_self._new_as_path_ties_is_better(self,
                                                           current_best_ann,
                                                           current_best_ann_processed,
                                                           new_ann,
                                                           new_ann_processed)




def _new_hole_size_is_smaller(policy_self, current_best_ann, new_ann):
    """Best by hole size"""

    # Holes aren't counted for this prefix
    if not hasattr(current_best_ann, "temp_holes"):
        return None

    if len(current_best_ann.temp_holes) > len(new_ann.temp_holes):
        return True
    elif len(current_best_ann.temp_holes) < len(new_ann.temp_holes):
        return False
    else:
        return None
