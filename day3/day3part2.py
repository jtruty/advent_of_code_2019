from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

wires: List[List[str]] = []
with open("input.txt") as f:
    for line in f:
        wires.append([d for d in line.strip().split(",")])


@dataclass
class Point:
    x: int
    y: int
    index: int

    def __hash__(self):
        return hash((self.x, self.y))

    def get_distance(self):
        return abs(self.x) + abs(self.y)


points: List[Dict[str, Point]] = []
min_intersect = None
min_point: Point = Point(0, 0, 0)


def check_intersect(point: Point):
    global min_intersect
    global min_point
    if points and f"{point.x}-{point.y}" in points[0]:
        if (
            not min_intersect
            or (points[0][f"{point.x}-{point.y}"].index + point.index) < min_intersect
        ):
            min_intersect = points[0][f"{point.x}-{point.y}"].index + point.index
            min_point = next_point


for wire in wires:
    start = Point(0, 0, 0)
    wire_points = {"0-0": start}
    idx = 1
    for point in wire:
        next_point = start
        if point[0] == "U":
            for y in range(start.y + 1, start.y + int(point[1:]) + 1):
                next_point = Point(start.x, y, idx)
                check_intersect(next_point)
                wire_points[f"{start.x}-{y}"] = next_point
                idx += 1
        elif point[0] == "D":
            for y in range(start.y - 1, start.y - int(point[1:]) - 1, -1):
                next_point = Point(start.x, y, idx)
                check_intersect(next_point)
                wire_points[f"{start.x}-{y}"] = next_point
                idx += 1
        elif point[0] == "R":
            for x in range(start.x + 1, start.x + int(point[1:]) + 1):
                next_point = Point(x, start.y, idx)
                check_intersect(next_point)
                wire_points[f"{x}-{start.y}"] = next_point
                idx += 1
        elif point[0] == "L":
            for x in range(start.x - 1, start.x - int(point[1:]) - 1, -1):
                next_point = Point(x, start.y, idx)
                check_intersect(next_point)
                wire_points[f"{x}-{start.y}"] = next_point
                idx += 1
        else:
            raise Exception("Not supported!")
        start = next_point  # new start is last point

    points.append(wire_points)

print(f"Min intersect point: {min_point}, distance: {min_intersect}")
