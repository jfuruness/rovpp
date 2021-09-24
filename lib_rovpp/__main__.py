from lib_bgp_simulator import Simulator, Graph, ROVPolicy, SubprefixHijack, BGPPolicy


from .rovpp_v1_lite_policy import ROVPPV1LitePolicy
from .rovpp_v2_lite_policy import ROVPPV2LitePolicy

def main():
    normal = [0, 5, 10, 20, 40, 60, 80, 100]
    quick = [20, 40, 60, 80]
    graphs = [Graph(percent_adoptions=normal,
                    adopt_policies=[ROVPPV1LitePolicy, ROVPolicy],
                    AttackCls=SubprefixHijack,
                    num_trials=50)]
    Simulator(debug=False).run(graphs=graphs, graph_path="/home/jmf/graphs.tar.gz")
