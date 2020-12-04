def get_required_fuel(mass: int) -> int:
    return (mass // 3) - 2


fuel_total = 0

with open("input.txt") as f:
    for input_line in f:
        fuel_required = get_required_fuel(int(input_line.strip()))
        while fuel_required >= 0:
            fuel_total += fuel_required
            fuel_required = get_required_fuel(fuel_required)

print(fuel_total)
