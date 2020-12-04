from dataclasses import dataclass
from typing import List, Set, Tuple

wires: List[List[str]] = []
with open("input.txt") as f:
    for line in f:
        wires.append([d for d in line.strip().split(",")])


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def get_distance(self):
        return abs(self.x) + abs(self.y)


points: List[Set[Point]] = []
min_intersect = None
min_point = None

for wire in wires:
    start = Point(0, 0)
    wire_points = [start]
    for point in wire:
        if point[0] == "U":
            next_points = [
                Point(start.x, y)
                for y in range(start.y + 1, start.y + int(point[1:]) + 1)
            ]
        elif point[0] == "D":
            next_points = [
                Point(start.x, y)
                for y in range(start.y - 1, start.y - int(point[1:]) - 1, -1)
            ]
        elif point[0] == "R":
            next_points = [
                Point(x, start.y)
                for x in range(start.x + 1, start.x + int(point[1:]) + 1)
            ]
        elif point[0] == "L":
            next_points = [
                Point(x, start.y)
                for x in range(start.x - 1, start.x - int(point[1:]) - 1, -1)
            ]
        else:
            raise Exception("Not supported!")
        wire_points.extend(next_points)
        start = next_points[-1]  # new start is last point
        print(start)

        # check for intersection
        if points:
            intersect = set(next_points).intersection(points[0])
            for intersect_point in intersect:
                distance = intersect_point.get_distance()
                if not min_intersect or distance < min_intersect:
                    min_intersect = distance
                    min_point = intersect_point

    points.append(set(wire_points))

print(f"Min intersect point: {min_point}, distance: {min_intersect}")
