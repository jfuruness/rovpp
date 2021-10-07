from datetime import datetime

from lib_bgp_simulator.engine.bgp_as import BGPAS
from lib_bgp_simulator.enums import ASNs, Prefixes, Timestamps, ROAValidity, Relationships
from lib_bgp_simulator.engine.simulator_engine import SimulatorEngine

#############################
# Functions
#############################

def shallow_assert_equal_ribs(asn, raw_rib, expected_rib):
    """
    These checks are mostly from lib_bgp_simulator local_ribs.py assert_eq method.
    https://github.com/jfuruness/lib_bgp_simulator
    Since this has been copied, the version in local_ribs.py may have changed.
    
    This version doesn't check the entire as_path, but rather just the 
    received_from_asn (i.e. one ASN deep into the as_path)
    """

    # Done this way to get specifics about what's different
    for prefix, ann in raw_rib.prefix_anns():
        expected_rib_ann = expected_rib.get(prefix, None)
        if expected_rib_ann is None:
            assert False, f"Simulator should not have {prefix} in ASN {asn}"
        assert expected_rib_ann.prefix == ann.prefix, f"Expected: {expected_rib_ann}\n Raw: {ann}"
        #assert expected_rib_ann.origin == ann.origin, f"Expected: {expected_rib_ann}\n Raw: {ann}"
        for i in range(len((expected_rib_ann.as_path[:2]))):
                assert ann.as_path[i] == expected_rib_ann.as_path[i], f"Expected: {expected_rib_ann}\n Raw: {ann}"
        #assert expected_rib_ann.timestamp == ann.timestamp, f"Expected: {expected_rib_ann}\n Raw: {ann}"
        assert expected_rib_ann.recv_relationship == ann.recv_relationship, f"Expected: {expected_rib_ann}\n Raw: {ann}"

    for prefix, ann in expected_rib.items():
        raw_rib_ann = raw_rib.get_ann(prefix)
        if raw_rib_ann is None:
            assert False, f"Simulator is missing {prefix} for ASN {asn}"
        else:
            assert raw_rib_ann.prefix == ann.prefix, f"Expected: {ann}\n Raw: {raw_rib_ann}"
            #assert raw_rib_ann.origin == ann.origin, f"Expected: {ann}\n Raw: {raw_rib_ann}"
            for i in range(len((ann.as_path[:2]))):
                assert raw_rib_ann.as_path[i] == ann.as_path[i], f"Expected: {ann}\n Raw: {raw_rib_ann}"
            #assert raw_rib_ann.timestamp == ann.timestamp, f"Expected: {ann}\n Raw: {raw_rib_ann}"
            assert raw_rib_ann.recv_relationship == ann.recv_relationship, f"Expected: {ann}\n Raw: {raw_rib_ann}"


#############################
# Main test function
#############################

# tmp_path is a pytest fixture
def run_example(peers=list(),
                customer_providers=list(),
                as_policies=dict(),
                announcements=list(),
                local_ribs=dict(),
                BaseASCls=BGPAS,
                attack_obj=None,
                as_path_check=False):
    """Runs an example"""

    print("populating engine")
    start = datetime.now()
    engine = SimulatorEngine(set(customer_providers),
                             set(peers),
                             BaseASCls=BaseASCls)
    for asn, as_policy in as_policies.items():
        engine.as_dict[asn].policy = as_policy()
    print((start-datetime.now()).total_seconds())
    print("Running engine")
    start = datetime.now()
    engine.run(announcements,attack=attack_obj)
    print((start-datetime.now()).total_seconds())
    if local_ribs:
        for as_obj in engine:
            print("ASN:", as_obj.asn)
            for prefix, ann in as_obj.policy.local_rib.prefix_anns():
                print(ann)
            if as_path_check: 
                as_obj.policy.local_rib == local_ribs[as_obj.asn]
            else:
                shallow_assert_equal_ribs(as_obj.asn, as_obj.policy.local_rib, local_ribs[as_obj.asn])

