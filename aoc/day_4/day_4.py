with open("aoc/day_4/input.txt", "r") as f:
    _input = f.read()


with open("aoc/day_4/test.txt", "r") as f:
    _test = f.read()

required_str = (
    "ecl:",
    "pid:",
    "eyr:",
    "hcl:",
    "byr:",
    "iyr:",
    # "cid:",
    "hgt:",
)

if __name__ == "__main__":
    # test part 1
    valid = 0
    passports = _test.split("\n\n")
    for p in passports:
        p_count = 0
        for req in required_str:
            if req in p:
                p_count += 1
        if p_count == len(required_str):
            valid += 1
    # print(f"TEST - Valid {valid} passports")
    print("TEST - Valid {} passports".format(valid))
    # prod part 1
    valid = 0
    passports = _input.split("\n\n")
    for p in passports:
        p_count = 0
        for req in required_str:
            if req in p:
                p_count += 1
        if p_count == len(required_str):
            valid += 1
    # print(f"PROD - Valid {valid} passports")
    print("TEST - Valid {} passports".format(valid))
