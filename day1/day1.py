def get_required_fuel(mass: int) -> int:
    return (mass // 3) - 2


fuel_total = 0

with open("input.txt") as f:
    for input_mass in f:
        fuel_total += get_required_fuel(int(input_mass.strip()))

print(fuel_total)
