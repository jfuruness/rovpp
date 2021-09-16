from copy import deepcopy

from ipaddress import ip_network

from lib_bgp_simulator import BGPPolicy, IncomingAnns, ROAValidity

from .blackhole import Blackhole


class ROVPPV1LitePolicy(BGPPolicy):

    name = "ROV++V1 Lite"

    def _propagate(policy_self, self, propagate_to, send_rels: list):
        """Propogates announcements from local rib to other ASes

        send_rels is the relationships that are acceptable to send

        Later you can change this so it's not the local rib that's
        being sent. But this is just proof of concept.
        """

        for as_obj in getattr(self, propagate_to.name.lower()):
            for prefix, ann in policy_self.local_rib.items():
                if ann.recv_relationship in send_rels and not isinstance(ann, Blackhole):
                    # Add the new ann to the incoming anns for that prefix
                    as_obj.policy.incoming_anns[prefix].append(ann)

    def process_incoming_anns(policy_self, self, recv_relationship):
        """Process all announcements that were incoming from a specific rel"""

        prefixes = policy_self.incoming_anns.keys()
        for prefix, ann_list in policy_self.incoming_anns.items():
            # Get announcement currently in local rib
            best_ann = policy_self.local_rib.get(prefix)

            # Done here to optimize
            if best_ann is not None and best_ann.seed_asn is not None:
                continue

            # For each announcement that was incoming
            for ann in ann_list:
                if ann.roa_validity == ROAValidity.INVALID:
                    continue
                # BGP Loop Prevention Check
                if self.asn in ann.as_path:
                    continue
                new_ann_is_better = policy_self._new_ann_is_better(self, best_ann, ann, recv_relationship)
                # If the new priority is higher
                if new_ann_is_better:
                    # Don't bother tiebreaking, if priority is same, keep existing
                    # Just like normal BGP
                    # Tiebreaking with time and such should go into the priority
                    # If we ever decide to do that
                    best_ann = deepcopy(ann)
                    best_ann.seed_asn = None
                    best_ann.as_path = (self.asn, *ann.as_path)
                    best_ann.recv_relationship = recv_relationship
                    # Save to local rib
                    policy_self.local_rib[prefix] = best_ann

        for prefix, ann in policy_self.local_rib.items():
            for potential_subprefix in prefixes:
                blackhole = False
                if ip_network(potential_subprefix).subnet_of(ip_network(prefix)):
                    for ann in policy_self.incoming_anns[potential_subprefix]:
                        if ann.roa_validity == ROAValidity.INVALID:
                            # NOTE: MUST make blackhole seed_asn to be true
                            # NOTE: must make blackhole identical 
                            policy_self.local_rib[prefix] = Blackhole(prefix=ann.prefix,
                                                                      timestamp=ann.timestamp,
                                                                      as_path=(self.asn,),
                                                                      seed_asn=self.asn,
                                                                      roa_validity=ROAValidity.INVALID)
                            blackhole = True
                            break
                if blackhole:
                    break

        policy_self.incoming_anns = IncomingAnns()
