from collections import deque
from typing import Dict, List, Set

graph: Dict[str, List[str]] = {}


def add_edge_node(node_1: str, node_2: str):
    if node_1 not in graph:
        graph[node_1] = [node_2]
    else:
        graph[node_1].append(node_2)


with open("input.txt") as f:
    for line in f:
        orbitee, orbiter = line.strip().split(")")
        add_edge_node(orbitee, orbiter)
        add_edge_node(orbiter, orbitee)


def find_shortest_path(lgraph: dict, start: str, end: str):
    dist = {start: [start]}
    q = deque([start])
    while len(q):
        at = q.popleft()
        for node in lgraph.get(at, []):
            if node not in dist:
                dist[node] = [dist[at], node]
                q.append(node)
    return dist.get(end)


def flatten(li):
    return sum(([x] if not isinstance(x, list) else flatten(x) for x in li), [])


print(graph)
path = flatten(find_shortest_path(graph, "YOU", "SAN"))
print(f"Shortest path: {path}")
dist = len(path)
print(f"Length: {dist - 3}")
