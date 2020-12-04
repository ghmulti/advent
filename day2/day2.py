import re

day2_lines = open("./day2/input.txt")
lines = day2_lines.readlines()

# print(lines)
print(len(lines))

p = re.compile("(\d+)\-(\d+) (\w):\s*(\w*)")

def parse_line(line):
    match = p.search(line)
    return {"source": line, "min": int(match.group(1)), "max": int(match.group(2)), "letter": match.group(3), "password": match.group(4).strip()}

parsed_lines = list(parse_line(line) for line in lines)
# print(list(parsed_lines))

##### part 1
def is_valid(line_parsed): 
    letter_num = line_parsed["password"].count(line_parsed["letter"])
    return letter_num >= line_parsed["min"] and letter_num <= line_parsed["max"]

valid_lines = (pline for pline in parsed_lines if is_valid(pline))
# print(list(valid_lines))
num_valid_lines = len(list(valid_lines))
print(num_valid_lines)

##### part 2
def is_valid_v2(line_parsed):
    pos1 = line_parsed["password"][line_parsed["min"] - 1]
    pos2 = line_parsed["password"][line_parsed["max"] - 1]
    return len([p for p in [pos1, pos2] if line_parsed["letter"] == p]) == 1

valid_lines_v2 = (pline for pline in parsed_lines if is_valid_v2(pline))
# print(list(valid_lines_v2))
num_valid_lines_v2 = len(list(valid_lines_v2))
print(num_valid_lines_v2)