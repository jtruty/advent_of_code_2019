from typing import Dict, Set

graph: Dict[str, Set[str]] = {}

with open("input.txt") as f:
    for line in f:
        orbitee, orbiter = line.strip().split(")")
        if orbitee not in graph:
            graph[orbitee] = {orbiter}
        else:
            graph[orbitee].add(orbiter)

counts: list = []


def traverse(node: str, count: int = 1):
    orbiters = graph.get(node)
    if not orbiters:
        return
    for orbiter in list(orbiters):
        print(f"Orbiter: {orbiter}, count: {count}")
        counts.append(count)
        traverse(orbiter, count + 1)


traverse("COM")
print(sum(counts))
