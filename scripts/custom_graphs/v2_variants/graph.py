from pathlib import Path

from bgpy.simulation_framework.graph_factory import GraphFactory


if __name__ == "__main__":
    output_dir: Path = Path("~/Desktop/graphs/").expanduser() / "v2_variants"
    pickle_path: Path = output_dir / "data.pickle"
    GraphFactory(
        pickle_path,
        output_dir / "graphs",
        label_replacement_dict={
            "ROV++V2_conference Simple": "ROV++V2_no_customers",
            "ROV++V2a Simple": "ROV++V2a",
            "ROV++V2 Shorten Simple": "ROV++V2_shorten",
            "ROV++V2 Journal Simple": "ROV++V2"
        }
    ).generate_graphs()
    print(f"\nWrote graphs to {output_dir / 'graphs'}")
