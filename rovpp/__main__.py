from argparse import ArgumentParser
from datetime import datetime
from frozendict import frozendict
from multiprocessing import Process, cpu_count
from pathlib import Path
import time

from bgpy import BGPSimpleAS
from bgpy import ROVSimpleAS
from bgpy import Simulation
from bgpy import SpecialPercentAdoptions  # noqa
from bgpy import ScenarioConfig

# Hijacks
from bgpy import SubprefixHijack
from bgpy import NonRoutedSuperprefixHijack
from bgpy import NonRoutedSuperprefixPrefixHijack
from bgpy import SuperprefixPrefixHijack
from bgpy import PrefixHijack
from bgpy import NonRoutedPrefixHijack

# Mixed deployment
from bgpy import get_real_world_rov_asn_cls_dict

# LITE
from .as_classes import ROVPPV1LiteSimpleAS

# NON LITE
from .as_classes import ROVPPV1SimpleAS
from .as_classes import ROVPPV2SimpleAS
from .as_classes import ROVPPV2aSimpleAS
from .as_classes import ROVPPV2ShortenSimpleAS
from .as_classes import ROVPPV2JournalSimpleAS
from .as_classes import ROVPPV3AS

from .rovpp_ann import ROVPPAnn


BASE_PATH = Path("~/Desktop/graphs/").expanduser()


def get_default_kwargs(quick, trials=None):  # pragma: no cover
    if not trials:
        trials = 1 if quick else 1000
    if quick:
        return {
            "percent_adoptions": (0.5,),
            "num_trials": trials,
            "parse_cpus": 1,
        }
    else:  # pragma: no cover
        return {
            "percent_adoptions": (
                0.001,  # SpecialPercentAdoptions.ONLY_ONE,  # .01,
                # 0.5,
                0.1,
                0.2,
                0.3,
                0.4,
                0.6,
                0.8,
                # .99],
                0.998,  # SpecialPercentAdoptions.ALL_BUT_ONE,
            ),
            "num_trials": trials,
            "parse_cpus": cpu_count() - 2,
            "caida_run_kwargs": {"dl_time": datetime(2023, 10, 5)},
            "python_hash_seed": 0,
        }


ROV_NON_LITE_ROVPP = (
    ROVSimpleAS,
    ROVPPV1SimpleAS,
    ROVPPV2JournalSimpleAS,
    # ROVPPV2aSimpleAS,
)


class V1Multi1(ROVPPV1SimpleAS):
    name = "ROV++V1 1 Attacker"


class V1Multi10(ROVPPV1SimpleAS):
    name = "ROV++V1 10 Attackers"


class V1Multi100(ROVPPV1SimpleAS):
    name = "ROV++V1 100 Attackers"


MULTI_ATK_AS_CLASSES = (V1Multi1, V1Multi10, V1Multi100)


class MixedV1SimpleAS(ROVPPV1SimpleAS):
    name = "Real World ROV nodes deploying V1 Simple"


class V1WV1SimpleAS(ROVPPV1SimpleAS):
    name = "ROV++V1 (V1 mixed)"


def run_simulation(
    sim,
):
    """See BGPy FAQ

    Long story short Each sim leaks memory due to some weird PyPy garbage collection
    that doesn't occur in Python. Running sims one after the other (for now)
    requires this. In the future we'll move to Rust, which has proper memory
    management.
    """

    print("Starting simulation")
    start = time.perf_counter()
    sim.run(
        graph_factory_kwargs={
            "label_replacement_dict": {
                # BGPy
                BGPSimpleAS.name: "BGP",
                ROVSimpleAS.name: "ROV",
                # ROV++
                ROVPPV1LiteSimpleAS.name: "ROV++V1 Lite",
                # NON LITE.name: "",
                ROVPPV1SimpleAS.name: "ROV++V1",
                ROVPPV2SimpleAS.name: "ROV++V2 No Customers",
                ROVPPV2aSimpleAS.name: "ROV++V2 Aggressive",
                ROVPPV2ShortenSimpleAS.name: "ROV++V2 Shorten",
                ROVPPV2JournalSimpleAS.name: "ROV++V2",
                ROVPPV3AS.name: "ROV++V3",
            },
            "y_axis_label_replacement_dict": {
                "PERCENT ATTACKER SUCCESS": "Data Plane % Hijacked",
                "PERCENT VICTIM SUCCESS": "Data Plane % Successfully Connected",
                "PERCENT DISCONNECTED": "Data Plane % Disconnected",
            },
            "x_axis_label_replacement_dict": {},
        }
    )
    print(f"{sim.output_dir} {(time.perf_counter() - start)}")


# Ignoring coverage on this func because it would cause every line
# to be covered, and there is a bare bones system test that just runs
# through these
def main(quick=True, trials=1, graph_index=None):  # pragma: no cover
    # assert isinstance(input("Turn asserts off for speed?"), str)
    sims = [
        Simulation(
            scenario_configs=tuple(
                [
                    ScenarioConfig(
                        ScenarioCls=SubprefixHijack, AdoptASCls=Cls, AnnCls=ROVPPAnn
                    )
                    for Cls in ROV_NON_LITE_ROVPP + (ROVPPV3AS,)
                ]
            ),
            output_dir=BASE_PATH / "subprefix",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
        Simulation(
            scenario_configs=tuple(
                [
                    ScenarioConfig(
                        ScenarioCls=SubprefixHijack,
                        AdoptASCls=ASCls,
                        AnnCls=ROVPPAnn,
                        num_attackers=num_attackers,
                    )
                    for (ASCls, num_attackers) in zip(
                        MULTI_ATK_AS_CLASSES, (1, 10, 100)
                    )
                ]
            ),
            output_dir=BASE_PATH / "subprefix_multi_atk",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
        Simulation(
            scenario_configs=tuple(
                [
                    ScenarioConfig(
                        ScenarioCls=NonRoutedPrefixHijack,
                        AdoptASCls=Cls,
                        AnnCls=ROVPPAnn,
                    )
                    for Cls in (
                        ROVPPV2SimpleAS,
                        ROVPPV2aSimpleAS,
                        ROVPPV2ShortenSimpleAS,
                        ROVPPV2JournalSimpleAS,
                    )
                ]
            ),
            output_dir=BASE_PATH / "v2_variants",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
        Simulation(
            scenario_configs=tuple(
                [
                    ScenarioConfig(
                        ScenarioCls=SubprefixHijack,
                        AdoptASCls=Cls,
                        AnnCls=ROVPPAnn,
                        hardcoded_asn_cls_dict=get_real_world_rov_asn_cls_dict(
                            min_rov_confidence=0
                        ),
                    )
                    for Cls in ROV_NON_LITE_ROVPP + (ROVPPV3AS,)
                ]
                + [
                    ScenarioConfig(
                        ScenarioCls=SubprefixHijack,
                        AdoptASCls=V1WV1SimpleAS,
                        AnnCls=ROVPPAnn,
                        hardcoded_asn_cls_dict=frozendict(
                            {
                                asn: MixedV1SimpleAS
                                for asn in get_real_world_rov_asn_cls_dict(
                                    min_rov_confidence=0
                                )
                            }
                        ),
                    ),
                ]
            ),
            output_dir=BASE_PATH / "mixed_deployment_rov",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
        Simulation(
            scenario_configs=tuple(
                [
                    ScenarioConfig(
                        ScenarioCls=NonRoutedSuperprefixHijack,
                        AdoptASCls=Cls,
                        AnnCls=ROVPPAnn,
                    )
                    for Cls in ROV_NON_LITE_ROVPP
                ]
            ),
            output_dir=BASE_PATH / "non_routed_superprefix",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
        Simulation(
            scenario_configs=tuple(
                [
                    ScenarioConfig(
                        ScenarioCls=SuperprefixPrefixHijack,
                        AdoptASCls=Cls,
                        AnnCls=ROVPPAnn,
                    )
                    for Cls in ROV_NON_LITE_ROVPP + (ROVPPV3AS,)
                ]
            ),
            output_dir=BASE_PATH / "superprefix_prefix",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
        Simulation(
            scenario_configs=tuple(
                [
                    ScenarioConfig(
                        ScenarioCls=PrefixHijack, AdoptASCls=Cls, AnnCls=ROVPPAnn
                    )
                    for Cls in ROV_NON_LITE_ROVPP
                ]
            ),
            output_dir=BASE_PATH / "prefix",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
        Simulation(
            scenario_configs=tuple(
                [
                    ScenarioConfig(
                        ScenarioCls=NonRoutedPrefixHijack,
                        AdoptASCls=Cls,
                        AnnCls=ROVPPAnn,
                    )
                    for Cls in ROV_NON_LITE_ROVPP
                ]
            ),
            output_dir=BASE_PATH / "non_routed_prefix",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
        Simulation(
            scenario_configs=tuple(
                [
                    ScenarioConfig(
                        ScenarioCls=NonRoutedSuperprefixPrefixHijack,
                        AdoptASCls=Cls,
                        AnnCls=ROVPPAnn,
                    )
                    for Cls in ROV_NON_LITE_ROVPP
                ]
            ),
            output_dir=BASE_PATH / "non_routed_superprefix_prefix",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
        Simulation(
            scenario_configs=tuple(
                [
                    ScenarioConfig(
                        ScenarioCls=SubprefixHijack,
                        AdoptASCls=Cls,
                        AnnCls=ROVPPAnn,
                    )
                    for Cls in (ROVPPV1SimpleAS, ROVPPV1LiteSimpleAS)
                ]
            ),
            output_dir=BASE_PATH / "lite_vs_non_lite",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
        Simulation(
            scenario_configs=tuple(
                [
                    ScenarioConfig(
                        ScenarioCls=SubprefixHijack,
                        AdoptASCls=Cls,
                        AnnCls=ROVPPAnn,
                    )
                    for Cls in (ROVSimpleAS,)
                ]
            ),
            output_dir=BASE_PATH / "ctrl_vs_data_plane",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
    ]

    if graph_index is not None:
        print(f"Running a sim for {sims[graph_index].output_dir.name}")
        run_simulation(sims[graph_index])
        return

    for sim in sims:
        if isinstance(sim, str):
            continue
        else:
            print("Spawning a sim process for {sim.output_dir.name}")
            # Create a Process for each simulation (see run_simulation for details)
            p = Process(target=run_simulation, args=(sim,))
            p.start()
            # Run one at a time due to resource constraints
            p.join()


if __name__ == "__main__":
    parser = ArgumentParser(description="Runs a simulation")
    parser.add_argument("--quick", dest="quick", default=False, action="store_true")
    parser.add_argument("--trials", type=int, dest="trials", default=1000)
    idx_default = -100
    parser.add_argument(
        "--graph_index", type=int, dest="graph_index", default=idx_default
    )
    args = parser.parse_args()
    graph_index = None if args.graph_index == idx_default else args.graph_index
    start = time.perf_counter()
    main(quick=args.quick, trials=args.trials, graph_index=graph_index)
    print((time.perf_counter() - start))
