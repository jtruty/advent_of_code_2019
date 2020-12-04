import sys
from enum import Enum
from intcode import IntCode
from typing import List

COLOR_BLACK = 0
COLOR_WHITE = 1

OUTPUT_TURN_LEFT = 0
OUTPUT_TURN_RIGHT = 1


def get_painted_grid(instructions: List[int], initial_color: int):
    intcode = IntCode(instructions)
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    position = (0, 0)
    point_colors: dict = {position: initial_color}
    result_direction = 0
    direction_idx = 0
    while result_direction is not None:
        intcode.with_input(
            point_colors[position] if position in point_colors else COLOR_BLACK
        )
        result_color = intcode.run_instructions()
        result_direction = intcode.run_instructions()
        if result_direction is not None:
            point_colors[position] = result_color
            direction_idx = (
                (direction_idx + 1)
                if result_direction == OUTPUT_TURN_RIGHT
                else (direction_idx - 1 + len(directions))
            ) % len(directions)
            position = (
                position[0] + directions[direction_idx][0],
                position[1] + directions[direction_idx][1],
            )
    return point_colors


def paint_output(painted_grid: dict):
    minx = min(painted_grid, key=lambda tile: tile[0])[0]
    maxx = max(painted_grid, key=lambda tile: tile[0])[0]

    miny = min(painted_grid, key=lambda tile: tile[1])[1]
    maxy = max(painted_grid, key=lambda tile: tile[1])[1]

    for y in range(miny, maxy + 1):
        row = ""
        for x in range(minx, maxx + 1):
            row += "#" if painted_grid.get((x, y)) == COLOR_WHITE else " "
        print(row)


instructions = IntCode.read_instructions(sys.argv[1])

print(f"Panels: {len(get_painted_grid(instructions.copy(), COLOR_BLACK))}")

paint_output(get_painted_grid(instructions.copy(), COLOR_WHITE))

