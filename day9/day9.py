from intcode import IntCode

INPUT_DEBUG = 1
INPUT_BOOST = 2

instructions = IntCode.read_instructions("input.txt")
intcode = IntCode(instructions).with_input(INPUT_BOOST)
result = 0
while result is not None:
    result = intcode.run_instructions()
    if result is not None:
        print(f"Output: {result}")
