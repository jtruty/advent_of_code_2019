from typing import List

instructions: List[int] = []
with open("input.txt") as f:
    for line in f:
        instructions.extend(int(num) for num in line.strip().split(","))


def execute_opcode(opcode: int, opcode_idx: int):
    if opcode == 1:
        result = (
            instructions[instructions[opcode_idx + 1]]
            + instructions[instructions[opcode_idx + 2]]
        )
    elif opcode == 2:
        result = (
            instructions[instructions[opcode_idx + 1]]
            * instructions[instructions[opcode_idx + 2]]
        )
    else:
        raise Exception(f"Unsupported opcode: {opcode} at index: {opcode_idx}")
    instructions[instructions[opcode_idx + 3]] = result


def run_instructions():
    idx = 0
    opcode = instructions[idx]
    while opcode != 99:
        execute_opcode(opcode, idx)
        idx += 4
        opcode = instructions[idx]


run_instructions()
print(instructions)
