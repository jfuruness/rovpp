from datetime import datetime

from lib_bgp_simulator.engine.bgp_as import BGPAS
from lib_bgp_simulator.enums import ASNs, Prefixes, Timestamps, ROAValidity, Relationships
from lib_bgp_simulator.engine.simulator_engine import SimulatorEngine

#############################
# Functions
#############################

def shallow_assert_equal_ribs(rib1, rib2):
    """
    These checks are mostly from lib_bgp_simulator local_ribs.py assert_eq method.
    https://github.com/jfuruness/lib_bgp_simulator
    Since this has been copied, the version in local_ribs.py may have changed.
    
    This version doesn't check the entire as_path, but rather just the 
    received_from_asn (i.e. one ASN deep into the as_path)
    """
    # Done this way to get specifics about what's different
    for prefix, ann in rib1.items():
        rib2_ann = rib2[prefix]
        assert rib2_ann.prefix == ann.prefix, f"{rib2_ann}, {ann}"
        assert rib2_ann.origin == ann.origin, f"{rib2_ann}, {ann}"
        if rib2_ann.recv_relationship  == Relationships.ORIGIN:
            assert rib2_ann.as_path[0] == ann.as_path[0], f"{rib2_ann}, {ann}"
        else:
            assert rib2_ann.as_path[1] == ann.as_path[1], f"{rib2_ann}, {ann}"
        assert rib2_ann.timestamp == ann.timestamp, f"{rib2_ann}, {ann}"
    for prefix, ann in rib2.items():
        rib1_ann = rib1[prefix]
        assert rib1_ann.prefix == ann.prefix, f"{rib1_ann}, {ann}"
        assert rib1_ann.origin == ann.origin, f"{rib1_ann}, {ann}"
        if rib1_ann.recv_relationship  == Relationships.ORIGIN:
            assert rib1_ann.as_path[0] == ann.as_path[0], f"{rib1_ann}, {ann}"
        else:
            assert rib1_ann.as_path[1] == ann.as_path[1], f"{rib1_ann}, {ann}"
        assert rib1_ann.timestamp == ann.timestamp, f"{rib1_ann}, {ann}"


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
            for prefix, ann in as_obj.policy.local_rib.items():
                print(ann)
            if as_path_check: 
                as_obj.policy.local_rib.assert_eq(local_ribs[as_obj.asn])
            else:
                shallow_assert_equal_ribs(as_obj.policy.local_rib, local_ribs[as_obj.asn])
