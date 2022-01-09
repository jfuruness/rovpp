from typing import Dict, Optional, Tuple

from lib_bgp_simulator import Announcement as Ann
from lib_bgp_simulator import ROVSimpleAS
from lib_bgp_simulator import EngineInput
from lib_bgp_simulator import Relationships


class ROVPPV1LiteSimpleAS(ROVSimpleAS):

    name = "ROV++V1 Lite Simple"

    __slots__ = tuple()

    def _policy_propagate(self, _, ann, *args):
        """Only propagate announcements that aren't blackholes"""

        # Policy handled this ann for propagation (and did nothing)
        return ann.blackhole

    def receive_ann(self, ann: Ann, *args, **kwargs):
        """Ensures that announcments are ROV++ and valid"""

        if not hasattr(ann, "blackhole"):
            raise NotImplementedError(
                "Policy can't handle announcements without blackhole attrs")
        return super(ROVPPV1LiteSimpleAS, self).receive_ann(
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
        super(ROVPPV1LiteSimpleAS, self).process_incoming_anns(
            from_rel,
            *args,
            propagation_round=propagation_round,
            engine_input=engine_input,
            reset_q=False,
            holes=holes,
            **kwargs)

        self._add_blackholes(holes, from_rel)

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
        #print(self.asn)
        #input(holes)
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
                        and not existing_local_rib_subprefix_ann.preventive)):
                    # If another entry exists, remove it
                    # if self._local_rib.get_ann(unprocessed_hole_ann.prefix):
                        # Remove current ann and replace with blackhole
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
                          holes=None,
                          **extra_kwargs):
        """Deep copies ann and modifies attrs"""

        # if ann.invalid_by_roa and not ann.preventive:
        #     extra_kwargs["blackhole"] = True
        #     extra_kwargs["traceback_end"] = True
        extra_kwargs["holes"] = holes[ann]
        return super(ROVPPV1LiteSimpleAS, self)._copy_and_process(
            ann, recv_relationship, **extra_kwargs)
