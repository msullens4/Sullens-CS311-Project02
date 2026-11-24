"""Supplied Project 2 behavioral checks. Keep unchanged; complete pathfinder.py."""
import copy
import random
import unittest
from CampusMap import WAYPOINTS, EDGES
from pathfinder import Graph, campus_route, dijkstra


def make_graph(nodes, edges):
    graph = Graph()
    for node in nodes:
        graph.add_node(node)
    for a, b, weight in edges:
        graph.add_edge(a, b, weight)
    return graph


def oracle(nodes, edges, start, closed=()):
    """Compute expected costs without calling the student routing functions."""
    distance = dict.fromkeys(nodes, float('inf'))
    distance[start] = 0
    for _ in range(len(nodes) - 1):
        changed = False
        for a, b, weight in edges:
            if frozenset((a, b)) in closed:
                continue
            for u, v in [(a, b), (b, a)]:
                candidate = distance[u] + weight
                if candidate < distance[v]:
                    distance[v] = candidate
                    changed = True
        if not changed:
            break
    return distance


class PathfinderChecks(unittest.TestCase):
    def assert_route(self, result, nodes, edges, start, end, closed=()):
        expected = oracle(nodes, edges, start, closed)[end]
        if expected == float('inf'):
            self.assertIsNone(result)
            return
        self.assertIsNotNone(result)
        cost, path = result
        self.assertTrue(path, 'reachable path must not be empty')
        self.assertEqual((path[0], path[-1]), (start, end))
        weights = {frozenset((a, b)): w for a, b, w in edges}
        total = 0
        for a, b in zip(path, path[1:]):
            edge = frozenset((a, b))
            self.assertIn(edge, weights, 'path contains a nonexistent edge')
            self.assertNotIn(edge, closed, 'path crosses a closed edge')
            total += weights[edge]
        self.assertEqual(cost, total, 'reported cost disagrees with path')
        self.assertEqual(cost, expected, 'route is not shortest')

    def test_map_and_both_directions(self):
        graph = make_graph(WAYPOINTS, EDGES)
        for a, b, w in EDGES:
            self.assertIn((b, w), graph.neighbors(a))
            self.assertIn((a, w), graph.neighbors(b))
        before = copy.deepcopy(graph.adjacency)
        graph.add_node('SCI')
        self.assertEqual(before, graph.adjacency, 'adding an existing node loses edges')

    def test_all_campus_pairs_and_closures(self):
        graph = make_graph(WAYPOINTS, EDGES)
        baseline = copy.deepcopy(graph.adjacency)
        for closure in [None, ('SCI', 'UC'), ('LIB', 'PAC')]:
            closed = set()
            if closure:
                graph.close_edge(*closure)
                closed.add(frozenset(closure))
            for src in WAYPOINTS:
                for dest in WAYPOINTS:
                    for function in [campus_route, dijkstra]:
                        self.assert_route(function(graph, src, dest), WAYPOINTS, EDGES, src, dest, closed)
            if closure:
                graph.reopen_edge(*closure)
            self.assertEqual(baseline, graph.adjacency)

    def test_closure_reopen_and_stored_result(self):
        graph = make_graph(WAYPOINTS, EDGES)
        old = campus_route(graph, 'SCI', 'UC')
        saved = copy.deepcopy(old)
        self.assertEqual(old[0], 3)
        graph.close_edge('UC', 'SCI')
        self.assertNotIn(('UC', 3), graph.neighbors('SCI'))
        self.assertNotIn(('SCI', 3), graph.neighbors('UC'))
        result = campus_route(graph, 'SCI', 'UC')
        self.assert_route(result, WAYPOINTS, EDGES, 'SCI', 'UC', {frozenset(('SCI', 'UC'))})
        self.assertEqual(result[0], 5)
        self.assertEqual(old, saved, 'new requests mutated a previously returned result')
        graph.reopen_edge('SCI', 'UC')
        self.assertEqual(campus_route(graph, 'SCI', 'UC')[0], 3)

    def test_disconnected_and_only_route_closed(self):
        nodes = ['BEC', 'SCI', 'ISOLATED']
        edges = [('BEC', 'SCI', 4)]
        graph = make_graph(nodes, edges)
        self.assertIsNone(campus_route(graph, 'BEC', 'ISOLATED'))
        self.assertEqual(campus_route(graph, 'ISOLATED', 'ISOLATED'), (0, ['ISOLATED']))
        graph.close_edge('BEC', 'SCI')
        self.assertIsNone(campus_route(graph, 'BEC', 'SCI'))
        graph.reopen_edge('SCI', 'BEC')
        self.assertEqual(campus_route(graph, 'BEC', 'SCI'), (4, ['BEC', 'SCI']))

    def test_improvement_and_zero_weight(self):
        nodes = ['BEC', 'SCI', 'LIB', 'UC']
        edges = [('BEC', 'SCI', 9), ('BEC', 'LIB', 1), ('LIB', 'SCI', 1), ('SCI', 'UC', 0)]
        graph = make_graph(nodes, edges)
        self.assert_route(campus_route(graph, 'BEC', 'UC'), nodes, edges, 'BEC', 'UC')
        self.assertEqual(campus_route(graph, 'BEC', 'UC')[0], 2)

    def test_generated_graphs_and_repeatability(self):
        rng = random.Random(31114)
        nodes = [f'N{i}' for i in range(6)]
        for trial in range(20):
            edges = [(a, b, rng.randint(0, 9)) for i, a in enumerate(nodes)
                     for b in nodes[i + 1:] if rng.random() < .4]
            graph = make_graph(nodes, edges)
            closed = set()
            if edges and trial % 2:
                a, b, _ = edges[0]
                graph.close_edge(a, b)
                closed.add(frozenset((a, b)))
            baseline = copy.deepcopy(graph.adjacency)
            for src in nodes:
                for dest in nodes:
                    self.assert_route(campus_route(graph, src, dest), nodes, edges, src, dest, closed)
            self.assertEqual(baseline, graph.adjacency)


if __name__ == '__main__':
    unittest.main()
