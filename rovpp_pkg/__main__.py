from argparse import ArgumentParser
from datetime import datetime
from multiprocessing import cpu_count
from pathlib import Path

from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import Simulation
from bgp_simulator_pkg import Subgraph
from bgp_simulator_pkg import SpecialPercentAdoptions

# Hijacks
from bgp_simulator_pkg import SubprefixHijack
from bgp_simulator_pkg import NonRoutedSuperprefixHijack
from bgp_simulator_pkg import SuperprefixPrefixHijack
from bgp_simulator_pkg import PrefixHijack
from bgp_simulator_pkg import NonRoutedPrefixHijack

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
        return {"percent_adoptions": [.5],
                "num_trials": trials,
                "subgraphs": [Cls() for Cls in Subgraph.subclasses
                              if Cls.name],
                "parse_cpus": 1}
    else:  # pragma: no cover
        return {"percent_adoptions": [SpecialPercentAdoptions.ONLY_ONE,  # .01,
                                      .5,
                                      .1,
                                      .2,
                                      .3,
                                      .4,
                                      .6,
                                      .8,
                                      # .99],
                                      SpecialPercentAdoptions.ALL_BUT_ONE],
                "num_trials": trials,
                "subgraphs": [Cls() for Cls in Subgraph.subclasses
                              if Cls.name],
                "parse_cpus": cpu_count() - 2}


ROV_NON_LITE_ROVPP = (ROVSimpleAS,
                      ROVPPV1SimpleAS,
                      ROVPPV2SimpleAS,
                      ROVPPV2aSimpleAS,)


# Ignoring coverage on this func because it would cause every line
# to be covered, and there is a bare bones system test that just runs
# through these
def main(quick=False, trials=1):  # pragma: no cover

    # assert isinstance(input("Turn asserts off for speed?"), str)

    sims = [Simulation(scenarios=tuple([SubprefixHijack(AdoptASCls=Cls,
                                                        AnnCls=ROVPPAnn,
                                                        min_rov_confidence=0)
                                        for Cls in
                                        ROV_NON_LITE_ROVPP + (ROVPPV3AS,)
                                        ]),
                       output_path=BASE_PATH / "mixed_deployment",
                       **get_default_kwargs(quick=quick, trials=trials)),
            Simulation(scenarios=tuple([SubprefixHijack(AdoptASCls=Cls,
                                                        AnnCls=ROVPPAnn)
                                        for Cls in
                                        ROV_NON_LITE_ROVPP + (ROVPPV3AS,)
                                        ]),
                       output_path=BASE_PATH / "subprefix",
                       **get_default_kwargs(quick=quick, trials=trials)),
            Simulation(scenarios=tuple(
                                  [NonRoutedSuperprefixHijack(AdoptASCls=Cls,
                                                              AnnCls=ROVPPAnn)
                                   for Cls in ROV_NON_LITE_ROVPP]),
                       output_path=BASE_PATH / "non_routed_superprefix",
                       **get_default_kwargs(quick=quick, trials=trials)),
            Simulation(scenarios=tuple([SuperprefixPrefixHijack(AdoptASCls=Cls,
                                                                AnnCls=ROVPPAnn
                                                                )
                                        for Cls in ROV_NON_LITE_ROVPP]),
                       output_path=BASE_PATH / "superprefix_prefix",
                       **get_default_kwargs(quick=quick, trials=trials)),
            Simulation(scenarios=tuple([PrefixHijack(AdoptASCls=Cls,
                                                     AnnCls=ROVPPAnn)
                                        for Cls in ROV_NON_LITE_ROVPP]),
                       output_path=BASE_PATH / "prefix",
                       **get_default_kwargs(quick=quick, trials=trials)),
            Simulation(scenarios=tuple([NonRoutedPrefixHijack(AdoptASCls=Cls,
                                                              AnnCls=ROVPPAnn)
                                        for Cls in ROV_NON_LITE_ROVPP]),
                       output_path=BASE_PATH / "non_routed_prefix",
                       **get_default_kwargs(quick=quick, trials=trials)),
            Simulation(scenarios=tuple([NonRoutedSuperprefixHijack(
                                    AdoptASCls=Cls,
                                    AnnCls=ROVPPAnn)
                                  for Cls in ROV_NON_LITE_ROVPP]),
                       output_path=BASE_PATH / "non_routed_superprefix_prefix",
                       **get_default_kwargs(quick=quick, trials=trials)),
            Simulation(scenarios=tuple([SubprefixHijack(AdoptASCls=Cls,
                                                        AnnCls=ROVPPAnn)
                                        for Cls in (ROVPPV1SimpleAS,
                                                    ROVPPV1LiteSimpleAS)]),
                       output_path=BASE_PATH / "lite_vs_non_lite",
                       **get_default_kwargs(quick=quick, trials=trials))]

    for sim in sims[:1]:
        start = datetime.now()
        sim.run()
        print(f"{sim.output_path} {(datetime.now() - start).total_seconds()}")


if __name__ == "__main__":

    parser = ArgumentParser(description="Runs a simulation")
    parser.add_argument("--quick",
                        dest="quick",
                        default=False,
                        action="store_true")
    parser.add_argument("--trials", type=int, dest="trials", default=1)
    args = parser.parse_args()
    start = datetime.now()
    main(quick=args.quick, trials=args.trials)
    print((datetime.now() - start).total_seconds())
