from datetime import datetime
from multiprocessing import cpu_count
from pathlib import Path

from bgp_simulator_pkg import ROVSimpleAS
from bgp_simulator_pkg import Simulation
from bgp_simulator_pkg import Subgraph

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


def get_default_kwargs(quick):  # pragma: no cover
    if quick:
        return {"percent_adoptions": [.5],
                "num_trials": 1,
                "subgraphs": [Cls() for Cls in Subgraph.subclasses
                              if Cls.name],
                "parse_cpus": 1}
    else:  # pragma: no cover
        return {"percent_adoptions": [0, .5, .1, .2, .3, .4, .6, .8, 1],
                "num_trials": 100,
                "subgraphs": [Cls() for Cls in Subgraph.subclasses
                              if Cls.name],
                "parse_cpus": cpu_count() // 2}


ROV_NON_LITE_ROVPP = (ROVSimpleAS,
                      ROVPPV1SimpleAS,
                      ROVPPV2SimpleAS,
                      ROVPPV2aSimpleAS,)


# Ignoring coverage on this func because it would cause every line
# to be covered, and there is a bare bones system test that just runs
# through these
def main(quick=True):  # pragma: no cover

    # assert isinstance(input("Turn asserts off for speed?"), str)

    sims = [Simulation(scenarios=tuple([SubprefixHijack(AdoptASCls=Cls,
                                                        AnnCls=ROVPPAnn)
                                        for Cls in
                                        ROV_NON_LITE_ROVPP + (ROVPPV3AS,)
                                        ]),
                       output_path=BASE_PATH / "subprefix",
                       **get_default_kwargs(quick=quick)),
            Simulation(scenarios=tuple(
                                  [NonRoutedSuperprefixHijack(AdoptASCls=Cls,
                                                              AnnCls=ROVPPAnn)
                                   for Cls in ROV_NON_LITE_ROVPP]),
                       output_path=BASE_PATH / "non_routed_superprefix",
                       **get_default_kwargs(quick=quick)),
            Simulation(scenarios=tuple([SuperprefixPrefixHijack(AdoptASCls=Cls,
                                                                AnnCls=ROVPPAnn
                                                                )
                                        for Cls in ROV_NON_LITE_ROVPP]),
                       output_path=BASE_PATH / "superprefix_prefix",
                       **get_default_kwargs(quick=quick)),
            Simulation(scenarios=tuple([PrefixHijack(AdoptASCls=Cls,
                                                     AnnCls=ROVPPAnn)
                                        for Cls in ROV_NON_LITE_ROVPP]),
                       output_path=BASE_PATH / "prefix",
                       **get_default_kwargs(quick=quick)),
            Simulation(scenarios=tuple([NonRoutedPrefixHijack(AdoptASCls=Cls,
                                                              AnnCls=ROVPPAnn)
                                        for Cls in ROV_NON_LITE_ROVPP]),
                       output_path=BASE_PATH / "non_routed_prefix",
                       **get_default_kwargs(quick=quick)),
            Simulation(scenarios=tuple([NonRoutedSuperprefixHijack(
                                    AdoptASCls=Cls,
                                    AnnCls=ROVPPAnn)
                                  for Cls in ROV_NON_LITE_ROVPP]),
                       output_path=BASE_PATH / "non_routed_superprefix_prefix",
                       **get_default_kwargs(quick=quick)),
            Simulation(scenarios=tuple([SubprefixHijack(AdoptASCls=Cls,
                                                        AnnCls=ROVPPAnn)
                                        for Cls in (ROVPPV1SimpleAS,
                                                    ROVPPV1LiteSimpleAS)]),
                       output_path=BASE_PATH / "lite_vs_non_lite",
                       **get_default_kwargs(quick=quick))]

    for sim in sims:
        start = datetime.now()
        sim.run()
        print(f"{sim.output_path} {(datetime.now() - start).total_seconds()}")


if __name__ == "__main__":
    start = datetime.now()
    main()
    print((datetime.now() - start).total_seconds())
