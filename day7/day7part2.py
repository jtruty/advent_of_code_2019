from itertools import permutations
from typing import List, Optional, Tuple

HALT = "99"
OUTPUT = "04"


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


def decode_opcode(instr_value: int):
    instr_value_str = str(instr_value).zfill(5)
    opcode = instr_value_str[3:5]
    first_param_immediate = is_immediate_mode(instr_value_str[2])
    second_param_immediate = is_immediate_mode(instr_value_str[1])
    result_param_immediate = is_immediate_mode(instr_value_str[0])
    return opcode, first_param_immediate, second_param_immediate, result_param_immediate


class IntCode:
    def __init__(self, instructions: List[int], phase: int):
        self.instructions = instructions
        self.ip = 0
        self.phase = phase
        self.phase_set = False
        self.prog_input = 0

    def with_input(self, the_input: int):
        self.prog_input = the_input
        return self

    def execute_instructions(self) -> Optional[int]:
        (
            opcode,
            first_param_immediate,
            second_param_immediate,
            result_param_immediate,
        ) = decode_opcode(self.instructions[self.ip])

        if opcode == "01":  # add
            result = get_instruction_param(
                self.ip + 1, first_param_immediate, self.instructions
            ) + get_instruction_param(
                self.ip + 2, second_param_immediate, self.instructions
            )
            self.instructions[self.instructions[self.ip + 3]] = result
            self.ip += 4
        elif opcode == "02":  # mul
            result = get_instruction_param(
                self.ip + 1, first_param_immediate, self.instructions
            ) * get_instruction_param(
                self.ip + 2, second_param_immediate, self.instructions
            )
            self.instructions[self.instructions[self.ip + 3]] = result
            self.ip += 4
        elif opcode == "03":  # input
            if self.phase_set:
                self.instructions[self.instructions[self.ip + 1]] = self.prog_input
            else:
                self.instructions[self.instructions[self.ip + 1]] = self.phase
                self.phase_set = True

            self.ip += 2
        elif opcode == OUTPUT:  # output, move to next amp
            output = get_instruction_param(
                self.ip + 1, first_param_immediate, self.instructions
            )
            self.ip += 2
            return output
        elif opcode == "05":  # jump if param is non-zero
            if (
                get_instruction_param(
                    self.ip + 1, first_param_immediate, self.instructions
                )
                != 0
            ):
                self.ip = get_instruction_param(
                    self.ip + 2, second_param_immediate, self.instructions
                )
            else:
                self.ip += 3
        elif opcode == "06":  # jump if false
            if (
                get_instruction_param(
                    self.ip + 1, first_param_immediate, self.instructions
                )
                == 0
            ):
                self.ip = get_instruction_param(
                    self.ip + 2, second_param_immediate, self.instructions
                )
            else:
                self.ip += 3
        elif opcode == "07":  # less than
            if get_instruction_param(
                self.ip + 1, first_param_immediate, self.instructions
            ) < get_instruction_param(
                self.ip + 2, second_param_immediate, self.instructions
            ):
                self.instructions[self.instructions[self.ip + 3]] = 1
            else:
                self.instructions[self.instructions[self.ip + 3]] = 0
            self.ip += 4
        elif opcode == "08":  # equals
            if get_instruction_param(
                self.ip + 1, first_param_immediate, self.instructions
            ) == get_instruction_param(
                self.ip + 2, second_param_immediate, self.instructions
            ):
                self.instructions[self.instructions[self.ip + 3]] = 1
            else:
                self.instructions[self.instructions[self.ip + 3]] = 0
            self.ip += 4
        elif opcode == HALT:
            return None
        else:
            raise Exception(f"Unsupported opcode: {opcode} at index: {self.ip}")
        return None

    def run_instructions(self) -> Optional[int]:
        (opcode, _, _, _,) = decode_opcode(self.instructions[self.ip])
        while opcode != HALT:
            result = self.execute_instructions()
            if result is not None:  # if output, return result
                return result
            (opcode, _, _, _,) = decode_opcode(self.instructions[self.ip])
        return None


instructions = read_instructions()
phases = permutations([5, 6, 7, 8, 9])
max_signal = 0
max_phase = None
for phase in phases:
    prog_input = 0
    amp = []
    for i in phase:
        amp.append({"program": IntCode(instructions.copy(), i), "halted": False})
    while not amp[-1]["halted"]:
        for a in amp:
            output = a["program"].with_input(prog_input).run_instructions()
            if output is None:
                a["halted"] = True
            else:
                prog_input = output
    if prog_input > max_signal:
        max_signal = prog_input
        max_phase = phase
    print(f"phase: {phase}, signal: {prog_input}")


print(f"Max signal: {max_signal}, phase: {max_phase}")
