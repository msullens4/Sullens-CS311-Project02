"""
Project 2: USI Pathfinder -- starter.

Complete Graph, dijkstra, and campus_route below. See
Project 2 USI Pathfinder.pdf for the assignment requirements.
"""

import heapq
from typing import Dict, List, Optional, Set, Tuple

Node = str
Edge = Tuple[Node, Node, float]


class Graph:
    """Weighted, undirected graph as an adjacency list."""

    def __init__(self) -> None:
        self.adjacency: Dict[Node, List[Tuple[Node, float]]] = {}
        # Keep closed pairs separate so reopening an edge restores access
        # without rebuilding the adjacency list.
        self.closed_edges: Set[frozenset] = set()

    def add_node(self, node: Node) -> None:
        # TODO
        raise NotImplementedError

    def add_edge(self, a: Node, b: Node, weight: float) -> None:
        """Add an undirected edge in both directions."""
        # TODO
        raise NotImplementedError

    def close_edge(self, a: Node, b: Node) -> None:
        """Mark the edge between a and b as closed (does not remove it from adjacency)."""
        # TODO
        raise NotImplementedError

    def reopen_edge(self, a: Node, b: Node) -> None:
        """Reopen the connection between a and b."""
        # TODO
        raise NotImplementedError

    def neighbors(self, node: Node) -> List[Tuple[Node, float]]:
        """Return (neighbor, weight) pairs for edges that are currently open."""
        # TODO
        raise NotImplementedError


def dijkstra(graph: Graph, start: Node, end: Node) -> Optional[Tuple[float, List[Node]]]:
    """
    Dijkstra's algorithm using a min-priority queue (heapq). Return
    (total_travel_time, ordered_path) or None if `end` is unreachable
    from `start`. Must skip stale priority-queue entries -- a popped
    distance that no longer matches the current best-known distance
    for that node.
    """
    # TODO
    raise NotImplementedError


def campus_route(map_graph: Graph, src: Node, dest: Node) -> Optional[Tuple[float, List[Node]]]:
    """
    Primary entry point tying the graph and Dijkstra together. Given
    the current state of `map_graph` (including any active closures),
    return the shortest route from `src` to `dest`.
    """
    # TODO
    raise NotImplementedError
