from dataclasses import dataclass
from math import sqrt
from typing import List, Set


@dataclass
class Asteroid:
    x: int
    y: int

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((x, y))


def get_distance_direction_vector(reference: Asteroid, b: Asteroid):
    distance = (b.x - reference.x, b.y - reference.y)
    norm = sqrt(distance[0] ** 2 + distance[1] ** 2)
    vector = (round(distance[0] / norm, 4), round(distance[1] / norm, 4))
    return norm, vector


def read_input(filename: str):
    asteroids: List[Asteroid] = []
    with open(filename) as f:
        for y_idx, line in enumerate(f):
            for x_idx, char in enumerate(line):
                if char == "#":
                    asteroids.append(Asteroid(x_idx, y_idx))
    return asteroids


def find_best_asteroid(asteroids: List[Asteroid]):
    max_line_of_sight = 0
    best_asteroid = None
    for asteroid in asteroids:
        vectors: set = set()
        for other_asteroid in asteroids:
            if asteroid == other_asteroid:
                continue
            vector = get_distance_direction_vector(other_asteroid, asteroid)[1]
            if vector not in vectors:
                vectors.add(vector)
        if len(vectors) > max_line_of_sight:
            max_line_of_sight = len(vectors)
            best_asteroid = asteroid
    return best_asteroid, max_line_of_sight


if __name__ == "__main__":
    best_asteroid, max_line_of_sight = find_best_asteroid(read_input("input.txt"))

    print(f"max line of sight: {max_line_of_sight}, best asteroid: {best_asteroid}")
