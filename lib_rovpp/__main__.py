from lib_bgp_simulator import Simulator, Graph, ROVPolicy, SubprefixHijack, BGPPolicy


from .rovpp_v1_lite_policy import ROVPPV1LitePolicy
from .rovpp_v2_lite_policy import ROVPPV2LitePolicy

def main():
    quick = True
    adoptions = [20] if quick else [0, 5, 10, 20, 40, 60, 80, 100]
    graphs = [Graph(percent_adoptions=adoptions,
                    adopt_policies=[ROVPPV1LitePolicy],
                    AttackCls=SubprefixHijack,
                    num_trials=1)]
    Simulator(debug=quick).run(graphs=graphs, graph_path="/home/jmf/graphs.tar.gz")
