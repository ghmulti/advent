import re
import inspect

lines = open("./day4/input.txt").readlines()
# print(lines)

def read_passports(lines, divider):
    passport = {}
    for line in lines:
        if line == divider:
            yield passport
            passport = {}
        entries = line.split()
        for entry in entries:
            (key,value) = entry.split(":")
            passport[key.strip()] = value.strip()
    yield passport

passports = list(read_passports(lines,'\n'))
# print(passports[-1:])
# print(f"Total number of passports {len(passports)}")

required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

strict_rules = [
    lambda p: p['byr'].isdigit() and 1920 <= int(p['byr']) <= 2002,
    lambda p: p['iyr'].isdigit() and 2010 <= int(p['iyr']) <= 2020,
    lambda p: p['eyr'].isdigit() and 2020 <= int(p['eyr']) <= 2030,
    lambda p: (p['hgt'].endswith("in") and p['hgt'][:-2].isdigit() and 59 <= int(p['hgt'][:-2]) <= 76) or (p['hgt'].endswith("cm") and p['hgt'][:-2].isdigit() and 150 <= int(p['hgt'][:-2]) <= 193),
    lambda p: re.match("^#[0-9a-f]{6}$", p['hcl']),
    lambda p: p['ecl'] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"],
    lambda p: re.match("^\d{9}$", p['pid'])
]

def validate_passport(passport):
    for field in required_fields:
        if field not in passport:
            # print(f"MISSING FIELD {field} for entry {passport}")
            return False
    return True

def validate_passport_strict(passport):
    for rule in strict_rules:
        if not rule(passport):
            # print(f"RULE FAILED {inspect.getsource(rule)} for entry {passport}")
            return False
    return True

#### part 1
valid_passports = list(filter(validate_passport, passports))
# print(valid_passports)
print(f"Number of valid passports: {len(valid_passports)}")

#### part 2
valid_passports_strict = list(filter(validate_passport_strict, valid_passports))
# print(valid_passports_strict)
print(f"Number of valid passports with strict rules: {len(valid_passports_strict)}")
