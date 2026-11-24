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
        if node not in self.adjacency:
            self.adjacency[node] = []

    def add_edge(self, a: Node, b: Node, weight: float) -> None:
        """Add an undirected edge in both directions."""
        # TODO
        if weight < 0:
            raise ValueError("Edge weights must be nonnegative.")

        self.add_node(a)
        self.add_node(b)

        self.adjacency[a].append((b, weight))
        self.adjacency[b].append((a, weight))
        
    def close_edge(self, a: Node, b: Node) -> None:
        """Mark the edge between a and b as closed (does not remove it from adjacency)."""
        # TODO
        self.closed_edges.add(frozenset((a, b)))

    def reopen_edge(self, a: Node, b: Node) -> None:
        """Reopen the connection between a and b."""
        # TODO
        self.closed_edges.discard(frozenset((a,b)))

    def neighbors(self, node: Node) -> List[Tuple[Node, float]]:
        """Return (neighbor, weight) pairs for edges that are currently open."""
        # TODO
        if node not in self.adjacency:
            return []

        return [
            (neighbor, weight)
            for neighbor, weight in self.adjacency[node]
            if frozenset((node, neighbor)) not in self.closed_edges
        ]

def dijkstra(graph: Graph, start: Node, end: Node) -> Optional[Tuple[float, List[Node]]]:
    """
    Dijkstra's algorithm using a min-priority queue (heapq). Return
    (total_travel_time, ordered_path) or None if `end` is unreachable
    from `start`. Must skip stale priority-queue entries -- a popped
    distance that no longer matches the current best-known distance
    for that node.
    """
    # TODO
    if start not in graph.adjacency or end not in graph.adjacency:
        return None

    if start == end:
        return(0, [start])

    distances: Dict[Node, float] = {
        node: float("inf")
        for node in graph.adjacency
    }

    parents: Dict[Node, Optional[Node]] = {
        node: None
        for node in graph.adjacency
    }

    distances[start] = 0

    heap: List[Tuple[float, Node]] = [(0, start)]

    while heap:
        current_distance, current = heapq.heappop(heap)

        if current_distance != distances[current]:
            continue

        if current == end:
            break

        for neighbor, weight in graph.neighbors(current):
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance 
                parents[neighbor] = current

                heapq.heappush(
                    heap,
                    (new_distance, neighbor)
                )
    if distances[end] == float("inf"):
        return None

    path: List[Node] = []
    current: Optional[Node] = end

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()

    return (distances[end], path)

def campus_route(map_graph: Graph, src: Node, dest: Node) -> Optional[Tuple[float, List[Node]]]:
    """
    Primary entry point tying the graph and Dijkstra together. Given
    the current state of `map_graph` (including any active closures),
    return the shortest route from `src` to `dest`.
    """
    # TODO
    return dijkstra(map_graph, src, dest)
