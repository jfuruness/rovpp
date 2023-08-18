from argparse import ArgumentParser
from datetime import datetime
from multiprocessing import cpu_count
from pathlib import Path

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
from .as_classes import ROVPPV3AS

from .rovpp_ann import ROVPPAnn


BASE_PATH = Path("~/Desktop/graphs/").expanduser()


def get_default_kwargs(quick, trials=None):  # pragma: no cover
    if not trials:
        trials = 1 if quick else 1500
    if quick:
        return {
            "percent_adoptions": (0.5,),
            "num_trials": trials,
            "parse_cpus": 1,
        }
    else:  # pragma: no cover
        return {
            "percent_adoptions": (
                0.01,  # SpecialPercentAdoptions.ONLY_ONE,  # .01,
                0.5,
                0.1,
                0.2,
                0.3,
                0.4,
                0.6,
                0.8,
                # .99],
                0.99,  # SpecialPercentAdoptions.ALL_BUT_ONE,
            ),
            "num_trials": trials,
            "parse_cpus": cpu_count() - 2,
        }


ROV_NON_LITE_ROVPP = (
    ROVSimpleAS,
    ROVPPV1SimpleAS,
    ROVPPV2SimpleAS,
    ROVPPV2aSimpleAS,
)


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
                        ScenarioCls=SubprefixHijack,
                        AdoptASCls=Cls,
                        AnnCls=ROVPPAnn,
                        hardcoded_asn_cls_dict=get_real_world_rov_asn_cls_dict(
                            min_rov_confidence=0
                        )
                    )
                    for Cls in ROV_NON_LITE_ROVPP + (ROVPPV3AS,)
                ]
            ),
            output_dir=BASE_PATH / "mixed_deployment",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
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
                    for Cls in ROV_NON_LITE_ROVPP
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
                        ScenarioCls=NonRoutedSuperprefixPrefixHijack,
                        AdoptASCls=Cls,
                        AnnCls=ROVPPAnn,
                    )
                    for Cls in (ROVPPV1SimpleAS, ROVPPV1LiteSimpleAS)
                ]
            ),
            output_dir=BASE_PATH / "lite_vs_non_lite",
            **get_default_kwargs(quick=quick, trials=trials),
        ),
    ]

    if graph_index is not None:
        sims = [sims[graph_index]]
    for sim in sims:
        print("starting sims")
        start = datetime.now()
        sim.run()
        print(f"{sim.output_dir} {(datetime.now() - start).total_seconds()}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Runs a simulation")
    parser.add_argument("--quick", dest="quick", default=False, action="store_true")
    parser.add_argument("--trials", type=int, dest="trials", default=1)
    idx_default = -100
    parser.add_argument(
        "--graph_index", type=int, dest="graph_index", default=idx_default
    )
    args = parser.parse_args()
    graph_index = None if args.graph_index == idx_default else args.graph_index
    start = datetime.now()
    main(quick=args.quick, trials=args.trials, graph_index=graph_index)
    print((datetime.now() - start).total_seconds())
