from typing import List

instructions: List[int] = []
with open("input.txt") as f:
    for line in f:
        instructions.extend(int(num) for num in line.strip().split(","))


def execute_opcode(opcode: int, opcode_idx: int, instructions: List[int]):
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


def run_instructions(instructions: List[int]):
    idx = 0
    opcode = instructions[idx]
    while opcode != 99:
        execute_opcode(opcode, idx, instructions)
        idx += 4
        opcode = instructions[idx]
    return instructions[0]


def find_output(instructions: List[int]):
    orig_instructions = instructions.copy()
    for int_1 in range(0, 100):
        for int_2 in range(0, 100):
            instructions[1] = int_1
            instructions[2] = int_2
            try:
                if run_instructions(instructions) == 19690720:
                    return 100 * int_1 + int_2
            except Exception as e:
                pass
            instructions = orig_instructions.copy()

    return None


print(find_output(instructions))
