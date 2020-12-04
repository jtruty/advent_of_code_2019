import sys
from dataclasses import dataclass
from math import acos, atan2, sqrt, pi
from typing import List
from day10 import (
    Asteroid,
    find_best_asteroid,
    get_distance_direction_vector,
    read_input,
)

TARGET_ASTEROID = 200


@dataclass
class AsteroidTarget:
    asteroid: Asteroid
    distance: float
    angle: float


def get_vector_angle(reference_vector: tuple, other_vector: tuple) -> float:
    dot_product = (
        reference_vector[0] * other_vector[0] + reference_vector[1] * other_vector[1]
    )
    return round(atan2(other_vector[0], other_vector[1]), 3,)


asteroids = read_input(sys.argv[1])
best_asteroid, _ = find_best_asteroid(asteroids)
reference_vector = (1, 0)
targets: List[AsteroidTarget] = []
for other_asteroid in asteroids:
    if best_asteroid == other_asteroid:
        continue
    distance, vector = get_distance_direction_vector(best_asteroid, other_asteroid)
    angle = get_vector_angle(reference_vector, vector)
    print(f"Asteroid: {other_asteroid}, vector: {vector}, angle: {angle}")
    targets.append(AsteroidTarget(other_asteroid, distance, angle))

targets.sort(key=lambda t: (t.angle, t.distance), reverse=True)
print(targets)
ordered_dict: dict = {}
for target in targets:
    if target.angle in ordered_dict:
        ordered_dict[target.angle].append(target)
    else:
        ordered_dict[target.angle] = [target]

count = 0
found = False
while not found:
    for angle, targets in ordered_dict.items():
        if targets:
            deleted = targets.pop(0)
            count += 1
            if count == TARGET_ASTEROID:
                print(
                    f"{TARGET_ASTEROID} target: {deleted}, answer: {deleted.asteroid.x * 100 + deleted.asteroid.y}"
                )
                found = True
                break

