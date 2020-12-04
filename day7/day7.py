from itertools import permutations
from typing import List, Optional, Tuple


def read_instructions() -> List[int]:
    instructions: List[int] = []
    with open("input.txt") as f:
        for line in f:
            instructions.extend(int(num) for num in line.strip().split(","))
    return instructions


def is_immediate_mode(mode: str):
    return mode == "1"


def get_instruction_param(idx: int, is_immediate: bool, instructions: List[int]) -> int:
    return instructions[idx] if is_immediate else instructions[instructions[idx]]


class IntCode:
    def __init__(self, instructions: List[int], phase: int, prog_input: int):
        self.instructions = instructions
        self.output: Optional[int] = None
        self.phase = phase
        self.phase_set = False
        self.prog_input = prog_input

    def execute_opcode(
        self, instr_value: int, opcode_idx: int, instructions: List[int]
    ) -> int:
        instr_value_str = str(instr_value).zfill(5)
        opcode = instr_value_str[3:5]
        first_param_immediate = is_immediate_mode(instr_value_str[2])
        second_param_immediate = is_immediate_mode(instr_value_str[1])
        result_param_immediate = is_immediate_mode(instr_value_str[0])

        if opcode == "01":  # add
            result = get_instruction_param(
                opcode_idx + 1, first_param_immediate, instructions
            ) + get_instruction_param(
                opcode_idx + 2, second_param_immediate, instructions
            )
            instructions[instructions[opcode_idx + 3]] = result
            return opcode_idx + 4
        if opcode == "02":  # mul
            result = get_instruction_param(
                opcode_idx + 1, first_param_immediate, instructions
            ) * get_instruction_param(
                opcode_idx + 2, second_param_immediate, instructions
            )
            instructions[instructions[opcode_idx + 3]] = result
            return opcode_idx + 4
        if opcode == "03":  # input
            if self.phase_set:
                instructions[instructions[opcode_idx + 1]] = self.prog_input
            else:
                instructions[instructions[opcode_idx + 1]] = self.phase
                self.phase_set = True

            return opcode_idx + 2
        if opcode == "04":  # output
            self.output = get_instruction_param(
                opcode_idx + 1, first_param_immediate, instructions
            )
            return opcode_idx + 2
        if opcode == "05":  # jump if param is non-zero
            if (
                get_instruction_param(
                    opcode_idx + 1, first_param_immediate, instructions
                )
                != 0
            ):
                return get_instruction_param(
                    opcode_idx + 2, second_param_immediate, instructions
                )
            return opcode_idx + 3
        if opcode == "06":  # jump if false
            if (
                get_instruction_param(
                    opcode_idx + 1, first_param_immediate, instructions
                )
                == 0
            ):
                return get_instruction_param(
                    opcode_idx + 2, second_param_immediate, instructions
                )
            return opcode_idx + 3
        if opcode == "07":  # less than
            if get_instruction_param(
                opcode_idx + 1, first_param_immediate, instructions
            ) < get_instruction_param(
                opcode_idx + 2, second_param_immediate, instructions
            ):
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

    def run_instructions(self) -> Optional[int]:
        idx = 0
        opcode = self.instructions[idx]
        while opcode != 99:
            idx = self.execute_opcode(opcode, idx, self.instructions)
            opcode = self.instructions[idx]
        return self.output


instructions = read_instructions()
phases = permutations([0, 1, 2, 3, 4])
max_signal = 0
max_phase = None
for phase in phases:
    prog_input = 0
    for i in phase:
        amp = IntCode(instructions.copy(), i, prog_input)
        amp.run_instructions()
        prog_input = amp.output if amp.output is not None else 0
    if prog_input > max_signal:
        max_signal = prog_input
        max_phase = phase
    print(f"phase: {phase}, signal: {prog_input}")


print(f"Max signal: {max_signal}, phase: {max_phase}")
