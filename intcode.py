from enum import Enum
from typing import List, Optional, Tuple

HALT = "99"
ADD = "01"
MUL = "02"
INPUT = "03"
OUTPUT = "04"
JUMP_NONZERO = "05"
JUMP_FALSE = "06"
LESS_THAN = "07"
EQUAL = "08"
RELATIVE_BASE_OFFSET = "09"


class ParamMode(str, Enum):
    POSITION = "0"
    IMMEDIATE = "1"
    RELATIVE = "2"


class IntCode:
    def __init__(self, instructions: List[int]):
        self.instructions = instructions
        self.ip = 0
        self.phase: Optional[int] = None
        self.phase_set = False
        self.prog_input = 0
        self.relative_instruction_offset = 0

    def with_input(self, the_input: int):
        self.prog_input = the_input
        return self

    def with_phase(self, phase: int):
        self.phase = phase
        return self

    @staticmethod
    def decode_opcode(instr_value: int):
        instr_value_str = str(instr_value).zfill(5)
        opcode = instr_value_str[3:5]
        first_param_mode = instr_value_str[2]
        second_param_mode = instr_value_str[1]
        result_param_mode = instr_value_str[0]
        return (
            opcode,
            first_param_mode,
            second_param_mode,
            result_param_mode,
        )

    @staticmethod
    def read_instructions(filename: str) -> List[int]:
        instructions: List[int] = []
        with open(filename) as f:
            for line in f:
                instructions.extend(int(num) for num in line.strip().split(","))
        instructions.extend([0] * 10 * len(instructions))  # double instructions size
        return instructions

    def _get_param_idx(self, idx: int, mode: str) -> int:
        if mode == ParamMode.IMMEDIATE:
            return idx
        if mode == ParamMode.POSITION:
            return self.instructions[idx]
        if mode == ParamMode.RELATIVE:
            return self.instructions[idx] + self.relative_instruction_offset

        raise Exception(f"Mode not supported: {mode}!")

    def _get_instruction_param(self, idx: int, mode: str) -> int:
        return self.instructions[self._get_param_idx(idx, mode)]

    def _execute_instructions(self) -> Optional[int]:
        (
            opcode,
            first_param_mode,
            second_param_mode,
            result_param_mode,
        ) = self.decode_opcode(self.instructions[self.ip])

        # print(f"Opcode: {opcode}, ip: {self.ip}")
        if opcode == ADD:
            result = self._get_instruction_param(
                self.ip + 1, first_param_mode
            ) + self._get_instruction_param(self.ip + 2, second_param_mode)
            self.instructions[
                self._get_param_idx(self.ip + 3, result_param_mode)
            ] = result
            self.ip += 4
        elif opcode == MUL:
            result = self._get_instruction_param(
                self.ip + 1, first_param_mode
            ) * self._get_instruction_param(self.ip + 2, second_param_mode)
            self.instructions[
                self._get_param_idx(self.ip + 3, result_param_mode)
            ] = result
            self.ip += 4
        elif opcode == INPUT:
            if self.phase is None or self.phase_set:
                input_val = self.prog_input
            else:
                input_val = self.phase
                self.phase_set = True
            self.instructions[
                self._get_param_idx(self.ip + 1, first_param_mode)
            ] = input_val
            self.ip += 2
        elif opcode == OUTPUT:
            output = self._get_instruction_param(self.ip + 1, first_param_mode)
            self.ip += 2
            return output
        elif opcode == JUMP_NONZERO:
            if self._get_instruction_param(self.ip + 1, first_param_mode) != 0:
                self.ip = self._get_instruction_param(self.ip + 2, second_param_mode)
            else:
                self.ip += 3
        elif opcode == JUMP_FALSE:
            if self._get_instruction_param(self.ip + 1, first_param_mode) == 0:
                self.ip = self._get_instruction_param(self.ip + 2, second_param_mode)
            else:
                self.ip += 3
        elif opcode == LESS_THAN:
            result = self._get_instruction_param(
                self.ip + 1, first_param_mode
            ) < self._get_instruction_param(self.ip + 2, second_param_mode)
            self.instructions[
                self._get_param_idx(self.ip + 3, result_param_mode)
            ] = int(result)
            self.ip += 4
        elif opcode == EQUAL:
            result = self._get_instruction_param(
                self.ip + 1, first_param_mode
            ) == self._get_instruction_param(self.ip + 2, second_param_mode)
            self.instructions[
                self._get_param_idx(self.ip + 3, result_param_mode)
            ] = int(result)
            self.ip += 4
        elif opcode == RELATIVE_BASE_OFFSET:
            self.relative_instruction_offset += self._get_instruction_param(
                self.ip + 1, first_param_mode
            )
            self.ip += 2
        elif opcode == HALT:
            return None
        else:
            raise Exception(f"Unsupported opcode: {opcode} at index: {self.ip}")
        return None

    def run_instructions(self) -> Optional[int]:
        (opcode, _, _, _,) = self.decode_opcode(self.instructions[self.ip])
        while opcode != HALT:
            result = self._execute_instructions()
            if result is not None:  # if output, return result
                return result
            (opcode, _, _, _,) = self.decode_opcode(self.instructions[self.ip])
        return None
