def is_possible_password(num: int) -> bool:
    has_adjacent_digits = False
    last_digit: str = "0"
    for digit in str(num):
        if digit == last_digit:
            has_adjacent_digits = True
        if int(digit) < int(last_digit):
            return False
        last_digit = digit
    return has_adjacent_digits


num_possible_passwords = 0
for num in range(235741, 706948 + 1):
    if is_possible_password(num):
        num_possible_passwords += 1

print(num_possible_passwords)
