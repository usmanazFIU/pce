import json
import unittest

import networkx as nx

from sdx.pce.load_balancing.te_solver import TESolver
from sdx.pce.utils.constants import Constants
from sdx.pce.utils.random_connection_generator import RandomConnectionGenerator
from sdx.pce.utils.random_topology_generator import RandomTopologyGenerator, dot_file

Connection = "./tests/data/test_connection.json"
topology_file = "./tests/data/Geant2012.dot"


class TESolverTests(unittest.TestCase):
    def make_random_graph(self, num_nodes=25, num_connections=3):
        graph_generator = RandomTopologyGenerator(
            num_node=num_nodes,
            link_probability=0.1,
            l_bw=10000,
            u_bw=50000,
            l_lat=10,
            u_lat=20,
            seed=2022,
        )
        graph = graph_generator.generate_graph()

        tm_generator = RandomConnectionGenerator(num_nodes=num_nodes)
        tm = tm_generator.generate_connection(
            querynum=num_connections,
            l_bw=5000,
            u_bw=15000,
            l_lat=50,
            u_lat=80,
            seed=2022,
        )

        return graph, tm

    def test_mc_solve(self):
        graph, tm = self.make_random_graph()
        print(f"tm: {tm}")

        solver = TESolver(graph, tm, Constants.COST_FLAG_HOP)
        path, result = solver.solve()
        ordered_paths = solver.solution_translator(path, result)

        print(f"Path: {ordered_paths}")
        print(f"Optimal: {result}")

        self.assertEqual(6.0, result)

    def test_lb_solve(self):
        graph, tm = self.make_random_graph()
        print(f"tm: {tm}")

        solver = TESolver(
            graph, tm, Constants.COST_FLAG_HOP, Constants.OBJECTIVE_LOAD_BALANCING
        )
        path, result = solver.solve()
        ordered_paths = solver.solution_translator(path, result)

        print(f"Path: {ordered_paths}")
        print(f"Optimal: {result}")

        # self.assertEqual(self.solution, path)
        self.assertEqual(1.851, round(result, 3))

    def test_mc_solve_5(self):
        graph = nx.read_edgelist(
            "./tests/data/test_five_node_topology.txt",
            nodetype=int,
            data=(
                ("weight", float),
                ("bandwidth", float),
                ("latency", float),
            ),
        )

        with open("./tests/data/test_five_node_request.json") as f:
            tm = json.load(f)

        solver = TESolver(graph, tm, Constants.COST_FLAG_HOP)
        path, result = solver.solve()
        ordered_paths = solver.solution_translator(path, result)

        print(f"Path: {ordered_paths}")
        print(f"Optimal: {result}")

        self.assertEqual(7.0, result)

    def test_mc_solve_geant2012(self):
        graph, tm = dot_file(topology_file, Connection)

        solver = TESolver(graph, tm, Constants.COST_FLAG_HOP)
        path, result = solver.solve()
        ordered_paths = solver.solution_translator(path, result)

        print(f"Path: {ordered_paths}")
        print(f"Optimal: {result}")


if __name__ == "__main__":
    unittest.main()
