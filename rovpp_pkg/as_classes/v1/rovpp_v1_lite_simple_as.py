from typing import Dict, Tuple

from bgp_simulator_pkg import Announcement as Ann
from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import Relationships
from bgp_simulator_pkg import Scenario

from ...rovpp_ann import ROVPPAnn


class ROVPPV1LiteSimpleAS(ROVSimpleAS):

    name = "ROV++V1 Lite Simple"

    def __init__(self, *args, **kwargs):
        super(ROVPPV1LiteSimpleAS, self).__init__(*args, **kwargs)
        self.temp_holes = dict()

    def _policy_propagate(self, _, ann, *args):
        """Only propagate announcements that aren't blackholes"""

        # Policy handled this ann for propagation (and did nothing)
        return ann.blackhole

    def receive_ann(self, ann: Ann, *args, **kwargs):
        """Ensures that announcments are ROV++ and valid"""

        if not isinstance(ann, ROVPPAnn):
            raise NotImplementedError("Not an ROV++ Announcement")
        return super(ROVPPV1LiteSimpleAS, self).receive_ann(
            ann, *args, **kwargs)

    def process_incoming_anns(self,
                              *,
                              from_rel: Relationships,
                              propagation_round: int,
                              scenario: "Scenario",
                              reset_q: bool = True):
        """Processes all incoming announcements"""

        self.temp_holes: Dict[Ann, Tuple[Ann]] = self._get_ann_to_holes_dict(
            scenario)
        super(ROVPPV1LiteSimpleAS, self).process_incoming_anns(
            from_rel,
            propagation_round=propagation_round,
            scenario=scenario,
            reset_q=False)
        self._add_blackholes(self.holes, from_rel)

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

    def _reset_q(self, reset_q: bool):
        if reset_q:
            self.temp_holes = dict()
        super(ROVPPV1LiteSimpleAS, self)._reset_q(reset_q)

    def _get_ann_to_holes_dict(self, engineinput):
        """Gets announcements to a typle of Ann holes

        Holes are subprefix hijacks
        """

        holes = dict()
        for _, ann_list in self._recv_q.prefix_anns():
            for ann in ann_list:
                ann_holes = []
                for subprefix in engineinput.prefix_subprefix_dict[ann.prefix]:
                    for sub_ann in self._recv_q.get_ann_list(subprefix):
                        # Holes are only from same neighbor
                        if (sub_ann.invalid_by_roa
                                and sub_ann.as_path[0] == ann.as_path[0]):
                            ann_holes.append(sub_ann)
                holes[ann] = tuple(ann_holes)
        return holes

    def _add_blackholes(self, holes, from_rel):
        """Manipulates local RIB by adding blackholes and dropping invalid"""

        blackholes_to_add = []
        # For each ann in local RIB:
        for _, ann in self._local_rib.prefix_anns():
            # For each hole in ann: (holes are invalid subprefixes)
            for unprocessed_hole_ann in ann.holes:
                # If there is not an existing valid ann for that hole subprefix
                existing_local_rib_subprefix_ann = self._local_rib.get_ann(
                    unprocessed_hole_ann.prefix)

                if (existing_local_rib_subprefix_ann is None
                    or (existing_local_rib_subprefix_ann.invalid_by_roa
                        and not existing_local_rib_subprefix_ann.preventive
                        # Without this line
                        # The same local rib Ann will try to create another
                        # blackhole for each from_rel
                        # But we don't want it to recreate
                        # And for single round prop, a future valid ann won't
                        # override the current valid ann due to gao rexford
                        and not existing_local_rib_subprefix_ann.blackhole)):
                    # If another entry exists, remove it
                    # if self._local_rib.get_ann(unprocessed_hole_ann.prefix):
                    #    # Remove current ann and replace with blackhole
                    #     self._local_rib.remove_ann(unprocessed_hole_ann.prefix)
                    # Create the blackhole
                    blackhole = self._copy_and_process(unprocessed_hole_ann,
                                                       from_rel,
                                                       holes=holes,
                                                       blackhole=True,
                                                       traceback_end=True)

                    blackholes_to_add.append(blackhole)
        # Do this here to avoid changing dict size
        for blackhole in blackholes_to_add:
            # Add the blackhole
            self._local_rib.add_ann(blackhole)
            # Do nothing - ann should already be a blackhole
            assert ((ann.blackhole and ann.invalid_by_roa)
                    or not ann.invalid_by_roa)

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

    def _process_outgoing_ann(self, neighbor, ann, *args, **kwargs):
        super(ROVPPV1LiteSimpleAS, self)._process_outgoing_ann(
            neighbor, ann.copy(holes=()), *args, **kwargs)
