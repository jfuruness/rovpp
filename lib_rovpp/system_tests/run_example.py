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
            assert expected_rib_ann.prefix == ann.prefix, f"At ASN: {asn}, Expected: {expected_rib_ann}\n Raw: {ann}"
        #assert expected_rib_ann.origin == ann.origin, f"At ASN: {asn}, Expected: {expected_rib_ann}\n Raw: {ann}"
        for i in range(len((expected_rib_ann.as_path[:2]))):
                assert ann.as_path[i] == expected_rib_ann.as_path[i], f"At ASN: {asn}, Expected: {expected_rib_ann}\n Raw: {ann}"
        #assert expected_rib_ann.timestamp == ann.timestamp, f"At ASN: {asn}, Expected: {expected_rib_ann}\n Raw: {ann}"
        assert expected_rib_ann.recv_relationship == ann.recv_relationship, f"At ASN: {asn}, Expected: {expected_rib_ann}\n Raw: {ann}"
        assert expected_rib_ann.blackhole == ann.blackhole, f"At ASN: {asn}, Expected RIB Blackhole Status is {expected_rib_ann.blackhole}: {expected_rib_ann}\n Raw RIB Blackhole Status is {ann.blackhole}: {ann}"


    for prefix, ann in expected_rib.items():
        raw_rib_ann = raw_rib.get_ann(prefix)
        if raw_rib_ann is None:
            assert False, f"Simulator is missing {prefix} for ASN {asn}"
        else:
            assert raw_rib_ann.prefix == ann.prefix, f"At ASN: {asn}, Expected: {ann}\n Raw: {raw_rib_ann}"
            #assert raw_rib_ann.origin == ann.origin, f"At ASN: {asn}, Expected: {ann}\n Raw: {raw_rib_ann}"
            for i in range(len((ann.as_path[:2]))):
                assert raw_rib_ann.as_path[i] == ann.as_path[i], f"At ASN: {asn}, Expected: {ann}\n Raw: {raw_rib_ann}"
            #assert raw_rib_ann.timestamp == ann.timestamp, f"At ASN: {asn}, Expected: {ann}\n Raw: {raw_rib_ann}"
            assert raw_rib_ann.recv_relationship == ann.recv_relationship, f"At ASN: {asn}, Expected: {ann}\n Raw: {raw_rib_ann}"
            assert raw_rib_ann.blackhole == ann.blackhole, f"At ASN: {asn}, Expected RIB Blackhole Status is {ann.blackhole}: {ann}\n Raw RIB Blackhole Status is {raw_rib_ann.blackhole}: {raw_rib_ann}"


#############################
# Main test function
#############################

# tmp_path is a pytest fixture
def run_example(peers=list(),
                customer_providers=list(),
                as_policies=dict(),
                announcements=list(),
                local_ribs=dict(),
                outcomes=dict(),
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
        engine.as_dict[asn].__class__ = as_policy
        engine.as_dict[asn].__init__(reset_base=False)
    print((start-datetime.now()).total_seconds())
    print("Running engine")
    start = datetime.now()
    engine.run(announcements,attack=attack_obj)
    print((start-datetime.now()).total_seconds())
    if local_ribs:
        for as_obj in engine:
            print("ASN: {0} ({1})".format(as_obj.asn, as_obj.name))
            print("computed local rib:")
            for prefix, ann in as_obj._local_rib.prefix_anns():
                print(ann)
            print("Actual local rib:")
            for prefix, ann in local_ribs[as_obj.asn].items():
                print(ann)
            # Check the RIBS against each other
            if as_path_check: 
                as_obj._local_rib == local_ribs[as_obj.asn]
            else:
                shallow_assert_equal_ribs(as_obj.asn, as_obj._local_rib, local_ribs[as_obj.asn])
    if outcomes:
        pass
