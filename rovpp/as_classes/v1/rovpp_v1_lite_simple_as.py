from typing import Dict, Tuple

from frozendict import frozendict

from bgpy.simulation_engine.announcement import Announcement as Ann  # noqa
from bgpy import ROVSimpleAS
from bgpy import Relationships
from bgpy import Scenario
from bgpy import (
    NonRoutedSuperprefixHijack,
    NonRoutedSuperprefixPrefixHijack,
)

from ...rovpp_ann import ROVPPAnn


class ROVPPV1LiteSimpleAS(ROVSimpleAS):
    name = "ROV++V1 Lite Simple"

    def __init__(self, *args, **kwargs):
        super(ROVPPV1LiteSimpleAS, self).__init__(*args, **kwargs)
        self.temp_holes = frozendict()

    def _policy_propagate(self, _, ann, *args) -> bool:
        """Only propagate announcements that aren't blackholes"""

        # Policy handled this ann for propagation (and did nothing)
        return bool(ann.blackhole)

    def receive_ann(self, ann: Ann, *args, **kwargs):  # type: ignore
        """Ensures that announcments are ROV++ and valid"""

        if not isinstance(ann, ROVPPAnn):
            raise NotImplementedError("Not an ROV++ Announcement")
        return super(ROVPPV1LiteSimpleAS, self).receive_ann(ann, *args, **kwargs)

    # Mypy errors out when getting subclass of this
    def process_incoming_anns(
        self,  # type: ignore
        *,
        from_rel: Relationships,
        propagation_round: int,
        scenario: "Scenario",
        reset_q: bool = True
    ):
        """Processes all incoming announcements"""

        # Super janky mutability garbage. Should be fixed later.
        self.temp_holes: Dict[
            Ann, Tuple[Ann]  # type: ignore
        ] = self._get_ann_to_holes_dict(scenario)
        super(ROVPPV1LiteSimpleAS, self).process_incoming_anns(
            from_rel=from_rel,
            propagation_round=propagation_round,
            scenario=scenario,
            reset_q=False,
        )
        self._add_blackholes(self.temp_holes, from_rel, scenario)

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

    # mypy can't subclass properly
    def _reset_q(self, reset_q: bool):  # type: ignore
        if reset_q:
            self.temp_holes = dict()
        super(ROVPPV1LiteSimpleAS, self)._reset_q(reset_q)

    def _get_ann_to_holes_dict(self, scenario: "Scenario"):
        """Gets announcements to a typle of Ann holes

        Holes are subprefix hijacks
        """

        holes = dict()
        for _, ann_list in self._recv_q.prefix_anns():
            for ann in ann_list:
                ann_holes = []
                for subprefix in scenario.ordered_prefix_subprefix_dict[ann.prefix]:
                    for sub_ann in self._recv_q.get_ann_list(subprefix):
                        # Holes are only from same neighbor
                        if (
                            sub_ann.invalid_by_roa
                            and sub_ann.as_path[0] == ann.as_path[0]
                        ):
                            ann_holes.append(sub_ann)
                # check all non routed announcements of the same prefix
                for same_prefix_ann in self._recv_q.get_ann_list(ann.prefix):
                    if (
                        same_prefix_ann.invalid_by_roa
                        and not same_prefix_ann.roa_routed
                        and same_prefix_ann.as_path[0] == ann.as_path[0]
                    ):
                        ann_holes.append(same_prefix_ann)
                holes[ann] = tuple(ann_holes)
        return frozendict(holes)

    def _add_blackholes(self, holes, from_rel, scenario):
        """Manipulates local RIB by adding blackholes and dropping invalid"""

        blackholes_to_add = []
        local_rib_to_remove = list()
        # For each ann in local RIB:
        for _, ann in self._local_rib.prefix_anns():
            # For each hole in ann: (holes are invalid subprefixes)
            for unprocessed_hole_ann in ann.holes:
                # If there is not an existing valid ann for that hole subprefix
                existing_local_rib_subprefix_ann = self._local_rib.get_ann(
                    unprocessed_hole_ann.prefix
                )

                if existing_local_rib_subprefix_ann is None or (
                    existing_local_rib_subprefix_ann.invalid_by_roa
                    and not existing_local_rib_subprefix_ann.preventive
                    # Without this line
                    # The same local rib Ann will try to create another
                    # blackhole for each from_rel
                    # But we don't want it to recreate
                    # And for single round prop, a future valid ann won't
                    # override the current valid ann due to gao rexford
                    and not existing_local_rib_subprefix_ann.blackhole
                ):
                    # If another entry exists, remove it
                    if self._local_rib.get_ann(unprocessed_hole_ann.prefix):
                        # Remove current ann and replace with blackhole
                        # These lines will only get hit if a subclass accepts
                        # invalid announcements and considers them valid
                        # which doesn't make sense, so won't bother testing
                        local_rib_to_remove.append(unprocessed_hole_ann.prefix)
                    # Create the blackhole
                    blackhole = self._copy_and_process(
                        unprocessed_hole_ann,
                        # Hole anns aren't processed, whereas ann's are,
                        # so anns have the correct relationship
                        ann.recv_relationship,
                        overwrite_default_kwargs={
                            # Aug 24 2023 just changed this from holes
                            # (which is a dict of ann: holes)
                            # To only the holes that are relevant for the ann
                            # (which is holes[ann])
                            # If this causes an error, just set it to (),
                            # Since for this paper and these specific simulations,
                            # the holes in blackholes don't matter at all
                            "holes": holes[unprocessed_hole_ann],
                            "blackhole": True,
                            "traceback_end": True,
                        },
                    )

                    blackholes_to_add.append(blackhole)

        for prefix in local_rib_to_remove:
            self._local_rib.remove_ann(prefix)  # TODO TEST

        # Must also add announcements that never made it into the local rib
        # Because the professors want to blackhole announcements even if ROV
        # Would have otherwise dropped them
        # For each ann in local RIB:
        for prefix, ann_list in self._recv_q.prefix_anns():
            # Don't go over announcements you've already checked in local rib
            if self._local_rib.get_ann(prefix):
                continue
            for ann in ann_list:
                # Get the anns that aren't routed and add them
                if not ann.roa_routed and ann.invalid_by_roa:
                    # Create the blackhole
                    blackhole = self._copy_and_process(
                        ann,
                        from_rel,
                        overwrite_default_kwargs={
                            "holes": (),
                            "blackhole": True,
                            "traceback_end": True,
                        },
                    )

                    blackholes_to_add.append(blackhole)

        # Hardcoded to blackhole superprefixes that we know exist
        # Professors wanted this change after we finished,
        # not worth the time to add correctly and they okayed this
        non_routed_superprefix_hijacks = (
            NonRoutedSuperprefixHijack,
            NonRoutedSuperprefixPrefixHijack,
        )
        if isinstance(scenario, non_routed_superprefix_hijacks):
            ann = self._local_rib.get_ann("1.0.0.0/8")
            if ann:
                bhole = self._copy_and_process(
                    ann,
                    ann.recv_relationship,
                    overwrite_default_kwargs={
                        "prefix": "1.2.0.0/16",
                        "holes": (),
                        "blackhole": True,
                        "traceback_end": True,
                    },
                )
                blackholes_to_add.append(bhole)
            # Add this new prefix to the dict for traceback
            # Keys must also be in order omg
            scenario.ordered_prefix_subprefix_dict = {
                "1.2.0.0/16": [],
                "1.0.0.0/8": ["1.2.0.0/16"],
            }

        # Do this here to avoid changing dict size
        for blackhole in blackholes_to_add:
            # Add the blackhole
            self._local_rib.add_ann(blackhole)
            # Do nothing - ann should already be a blackhole
            assert (
                blackhole.blackhole and blackhole.invalid_by_roa
            ) or not blackhole.invalid_by_roa

    def _copy_and_process(self, ann, recv_relationship, overwrite_default_kwargs=None):
        """Deep copies ann and modifies attrs"""

        if overwrite_default_kwargs:  # noqa
            # This is a no op for us, but for future subclasses it might
            # encounter this line of code. Omitting coverage to save time
            if "holes" not in overwrite_default_kwargs:  # pragma: no cover
                overwrite_default_kwargs["holes"] = self.temp_holes[ann]
        else:
            overwrite_default_kwargs = {"holes": self.temp_holes[ann]}

        return super(ROVPPV1LiteSimpleAS, self)._copy_and_process(
            ann, recv_relationship, overwrite_default_kwargs=overwrite_default_kwargs
        )

    def _process_outgoing_ann(self, neighbor, ann, *args, **kwargs):
        no_holes_ann = ann.copy(overwrite_default_kwargs={"holes": ()})
        super(ROVPPV1LiteSimpleAS, self)._process_outgoing_ann(
            neighbor, no_holes_ann, *args, **kwargs
        )
