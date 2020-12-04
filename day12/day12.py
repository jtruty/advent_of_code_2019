import re, sys
from dataclasses import dataclass
from typing import List


@dataclass
class Moon:
    x_pos: int
    y_pos: int
    z_pos: int

    x_vel: int = 0
    y_vel: int = 0
    z_vel: int = 0

    def __eq__(self, other):
        return (
            self.x_pos == other.x_pos
            and self.y_pos == other.y_pos
            and self.z_pos == other.z_pos
            and self.x_vel == other.x_vel
            and self.y_vel == other.y_vel
            and self.z_vel == other.z_vel
        )

    def __hash__(self):
        return hash(
            (self.x_pos, self.y_pos, self.z_pos, self.x_vel, self.y_vel, self.z_vel)
        )


@dataclass
class MoonList:
    moons: List[Moon]

    def __hash__(self):
        return sum([hash(moon) for moon in self.moons])


def read_input(filename: str):
    moons: list = []
    with open(filename) as f:
        for line in f:
            result = re.match("<x=(-?\d+), y=(-?\d+), z=(-?\d+)>", line.strip())
            if result:
                moons.append(
                    Moon(
                        int(result.group(1)), int(result.group(2)), int(result.group(3))
                    )
                )
    return moons


def apply_gravity(moons: List[Moon]):
    for moon in moons:
        for other_moon in moons:
            if moon == other_moon:
                continue
            if moon.x_pos > other_moon.x_pos:
                moon.x_vel -= 1
            elif moon.x_pos < other_moon.x_pos:
                moon.x_vel += 1

            if moon.y_pos > other_moon.y_pos:
                moon.y_vel -= 1
            elif moon.y_pos < other_moon.y_pos:
                moon.y_vel += 1

            if moon.z_pos > other_moon.z_pos:
                moon.z_vel -= 1
            elif moon.z_pos < other_moon.z_pos:
                moon.z_vel += 1


def apply_velocity(moons: List[Moon]):
    for moon in moons:
        moon.x_pos = moon.x_pos + moon.x_vel
        moon.y_pos = moon.y_pos + moon.y_vel
        moon.z_pos = moon.z_pos + moon.z_vel


def calc_energy(moons: List[Moon]):
    energy = 0
    for moon in moons:
        energy += (abs(moon.x_pos) + abs(moon.y_pos) + abs(moon.z_pos)) * (
            abs(moon.x_vel) + abs(moon.y_vel) + abs(moon.z_vel)
        )
    return energy


moon_list = MoonList(read_input(sys.argv[1]))
steps = int(sys.argv[2])
seen: set = {moon_list}
for step in range(steps):
    apply_gravity(moon_list.moons)
    apply_velocity(moon_list.moons)
    if moon_list in seen:
        print(f"Steps to repeat: {step+1}")
        break
    # seen.add(moon_list)

print(f"Energy: {calc_energy(moon_list.moons)}")
