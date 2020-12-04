def is_possible_password(num: int) -> bool:
    has_adjacent_digits = False
    found_digits = False
    consecutive_digits = 1
    last_digit: str = "-1"
    for digit in str(num):
        if not found_digits and digit == last_digit:
            if consecutive_digits > 1:
                has_adjacent_digits = False
            else:
                has_adjacent_digits = True
            consecutive_digits += 1
        else:
            if has_adjacent_digits:
                found_digits = True
            consecutive_digits = 1
        if int(digit) < int(last_digit):
            return False
        last_digit = digit
    return has_adjacent_digits


num_possible_passwords = 0
for num in range(235741, 706948 + 1):
    if is_possible_password(num):
        num_possible_passwords += 1

print(num_possible_passwords)
