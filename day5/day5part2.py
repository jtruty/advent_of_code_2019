from typing import List

PROGRAM_INPUT_VAL = 5
instructions: List[int] = []
with open("input.txt") as f:
    for line in f:
        instructions.extend(int(num) for num in line.strip().split(","))


def is_immediate_mode(mode: str):
    return mode == "1"


def get_instruction_param(idx: int, is_immediate: bool, instructions: List[int]) -> int:
    return instructions[idx] if is_immediate else instructions[instructions[idx]]


def execute_opcode(instr_value: int, opcode_idx: int, instructions: List[int]) -> int:
    instr_value_str = str(instr_value).zfill(5)
    opcode = instr_value_str[3:5]
    first_param_immediate = is_immediate_mode(instr_value_str[2])
    second_param_immediate = is_immediate_mode(instr_value_str[1])
    result_param_immediate = is_immediate_mode(instr_value_str[0])

    if opcode == "01":  # add
        result = get_instruction_param(
            opcode_idx + 1, first_param_immediate, instructions
        ) + get_instruction_param(opcode_idx + 2, second_param_immediate, instructions)
        instructions[instructions[opcode_idx + 3]] = result
        return opcode_idx + 4
    if opcode == "02":  # mul
        result = get_instruction_param(
            opcode_idx + 1, first_param_immediate, instructions
        ) * get_instruction_param(opcode_idx + 2, second_param_immediate, instructions)
        instructions[instructions[opcode_idx + 3]] = result
        return opcode_idx + 4
    if opcode == "03":  # input
        instructions[instructions[opcode_idx + 1]] = PROGRAM_INPUT_VAL
        return opcode_idx + 2
    if opcode == "04":  # output
        print(
            f"Program Output: {get_instruction_param(opcode_idx + 1, first_param_immediate, instructions)}"
        )
        return opcode_idx + 2
    if opcode == "05":  # jump if param is non-zero
        if (
            get_instruction_param(opcode_idx + 1, first_param_immediate, instructions)
            != 0
        ):
            return get_instruction_param(
                opcode_idx + 2, second_param_immediate, instructions
            )
        return opcode_idx + 3
    if opcode == "06":  # jump if false
        if (
            get_instruction_param(opcode_idx + 1, first_param_immediate, instructions)
            == 0
        ):
            return get_instruction_param(
                opcode_idx + 2, second_param_immediate, instructions
            )
        return opcode_idx + 3
    if opcode == "07":  # less than
        if get_instruction_param(
            opcode_idx + 1, first_param_immediate, instructions
        ) < get_instruction_param(opcode_idx + 2, second_param_immediate, instructions):
            instructions[instructions[opcode_idx + 3]] = 1
        else:
            instructions[instructions[opcode_idx + 3]] = 0
        return opcode_idx + 4
    if opcode == "08":  # equals
        if get_instruction_param(
            opcode_idx + 1, first_param_immediate, instructions
        ) == get_instruction_param(
            opcode_idx + 2, second_param_immediate, instructions
        ):
            instructions[instructions[opcode_idx + 3]] = 1
        else:
            instructions[instructions[opcode_idx + 3]] = 0
        return opcode_idx + 4
    raise Exception(f"Unsupported opcode: {opcode} at index: {opcode_idx}")


def run_instructions(instructions: List[int]):
    idx = 0
    opcode = instructions[idx]
    while opcode != 99:
        idx = execute_opcode(opcode, idx, instructions)
        opcode = instructions[idx]


run_instructions(instructions)
