from collections import defaultdict
from itertools import product
from pathlib import Path
import pickle

import matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore

from bgpy.simulation_framework.metric_tracker.metric_key import MetricKey
from bgpy.simulation_framework.utils import get_all_metric_keys

from bgpy.enums import SpecialPercentAdoptions, Outcomes, ASGroups, Plane


# NOTE: The raw data has only ROV adopting for subprefix hijack

class CtrlVsDataGraph:
    """Automates graphing of default graphs"""

    def __init__(self, pickle_path: Path, graph_dir: Path) -> None:
        self.pickle_path: Path = pickle_path
        with self.pickle_path.open("rb") as f:
            self.graph_rows = pickle.load(f)
        self.graph_dir: Path = graph_dir
        self.graph_dir.mkdir(parents=True, exist_ok=True)

    def generate_graphs(self) -> None:
        """Generates default graphs"""

        # Each metric key here contains plane, as group, and outcome
        # In other words, aech type of graph

        # List of (metric_key, adopting)
        graph_infos = list(product(get_all_metric_keys(), [True, False]))

        relevant_rows = list()
        for metric_key, adopting in graph_infos:
            for row in self.graph_rows:
                # Get all the rows that correspond to that type of graph
                BaseASCls = row["data_key"].scenario_config.BaseASCls
                AdoptASCls = row["data_key"].scenario_config.AdoptASCls
                if (
                    # row["metric_key"].plane == metric_key.plane and
                    row["metric_key"].plane == Plane.DATA and
                    # row["metric_key"].as_group == metric_key.as_group
                    row["metric_key"].as_group == ASGroups.ALL
                    # and row["metric_key"].outcome == metric_key.outcome
                    and row["metric_key"].outcome == Outcomes.ATTACKER_SUCCESS
                    and (
                        (row["metric_key"].ASCls == BaseASCls and not adopting)
                        or (row["metric_key"].ASCls == AdoptASCls and adopting)
                    )
                ):
                    relevant_rows.append((row, adopting))
        self._generate_graph(metric_key, relevant_rows, adopting=adopting)

    def _generate_graph(self, metric_key: MetricKey, _relevant_rows, adopting) -> None:
        """Writes a graph to the graph dir"""

        # Row is:
        # data_key: DataKey
        #    propagation_round
        #    percent_adopt
        #    scenario_config
        # metric_key: MetricKey
        #     Plane
        #     as_group
        #     outcome
        #     ASCls
        # Value: float
        # Yerr: yerr

        # Janky I know
        relevant_rows = [x[0] for x in _relevant_rows]

        if not relevant_rows:
            return
        graph_name = "lite_vs_non_lite.png"
        #    f"{relevant_rows[0]['data_key'].scenario_config.ScenarioCls.__name__}"
        #    f"/{metric_key.as_group.value}_adopting_is_{adopting}"
        #    f"/{metric_key.outcome.name}"
        #    f"_{metric_key.plane.value}.png"
        #).replace(" ", "")
        as_cls_rows_dict = defaultdict(list)
        for row, adopting in _relevant_rows:
            adopt_str = "adopting" if adopting else "non_adopting"
            as_cls_str = row["data_key"].scenario_config.AdoptASCls.name
            key = f"{as_cls_str}_{adopt_str}"
            as_cls_rows_dict[key].append(row)

        matplotlib.use("Agg")
        fig, ax = plt.subplots()
        fig.set_dpi(150)
        # Set X and Y axis size
        plt.xlim(0, 100)
        plt.ylim(0, 100)

        def get_percent_adopt(graph_row) -> float:
            """Extractions percent adoption for sort comparison

            Need separate function for mypy puposes
            """

            percent_adopt = graph_row["data_key"].percent_adopt
            assert isinstance(percent_adopt, (float, SpecialPercentAdoptions))
            return float(percent_adopt)

        # Add the data from the lines
        for key, graph_rows in as_cls_rows_dict.items():
            graph_rows_sorted = list(sorted(graph_rows, key=get_percent_adopt))
            ax.errorbar(
                [float(x["data_key"].percent_adopt) * 100 for x in graph_rows_sorted],
                [x["value"] for x in graph_rows_sorted],
                yerr=[x["yerr"] for x in graph_rows_sorted],
                label=key,
            )
        # Set labels
        ax.set_ylabel("PERCENT HIJACKED")
        ax.set_xlabel("Percent Adoption")

        # This is to avoid warnings
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        plt.tight_layout()
        plt.rcParams.update({"font.size": 14, "lines.markersize": 10})
        (self.graph_dir / graph_name).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(self.graph_dir / graph_name)
        # https://stackoverflow.com/a/33343289/8903959
        plt.close(fig)

pickle_path = Path("~/Desktop/graphs/lite_vs_non_lite/data.pickle").expanduser()
graph_dir = Path("~/Desktop/custom_rovpp_graphs").expanduser()
CtrlVsDataGraph(
    pickle_path=pickle_path,
    graph_dir=graph_dir,
).generate_graphs()
