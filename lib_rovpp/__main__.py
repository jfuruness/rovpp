from lib_bgp_simulator import Simulator, Graph, ROVPolicy, SubprefixHijack, BGPPolicy


from .rovpp_v1_lite_policy import ROVPPV1LitePolicy
from .rovpp_v2_lite_policy import ROVPPV2LitePolicy

def main():
    graphs = [Graph(percent_adoptions=[5, 10, 20, 30, 40, 60, 80, 100],
                    adopt_policies=[ROVPPV2LitePolicy, ROVPolicy, ROVPPV1LitePolicy],
                    AttackCls=SubprefixHijack,
                    num_trials=1)]
    Simulator(debug=True).run(graphs=graphs, graph_path="/home/jmf/graphs.tar.gz")
