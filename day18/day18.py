
lines = open("./day18/input.txt").read().splitlines()
# print(lines[0])

def find_nested(line):
    startindex = 0
    for index,l in enumerate(line):
        if l == "(":
            startindex = index
        if l == ")":
            return line[startindex:index+1]
    return None

assert find_nested("1 + ((1 + 2 + (3 * 1)))") == "(3 * 1)"

def calculate_nested(line, calculate_simple_fn):
    nested = find_nested(line)
    if nested:
        expr = nested[1:-1]
        result = calculate_simple_fn(expr.split())
        return calculate_nested(line=line.replace(nested, str(result)), calculate_simple_fn=calculate_simple_fn)
    else:
        return calculate_simple_fn(line.split())

print("==== Part 1 ====")

def calculate_simple_v1(entries):
    result = eval(f"{entries[0]} {entries[1]} {entries[2]}")    
    if len(entries) > 3:
        return calculate_simple_v1([result] + entries[3:])
    else:
        return result

assert calculate_simple_v1("1 + 2 * 3 + 4 * 5 + 6".split()) == 71

parsed_lines_1 = list(calculate_nested(line=line, calculate_simple_fn=calculate_simple_v1) for line in lines)
result_1 = sum(parsed_lines_1)
print(f"Sum of results = {result_1}")

assert result_1 == 86311597203806


print("==== Part 2 ====")

def calculate_simple_v2(entries):
    if len(entries) == 1:
        return entries[0]

    index = next((index for index, entry in enumerate(entries) if entry == "+"), None)
    if index is None:
        return calculate_simple_v1(entries)
    else:
        result = eval(f"{entries[index-1]} + {entries[index+1]}")
        new_entries = entries[:index-1] + [result] + entries[index+2:]
        return calculate_simple_v2(new_entries)

assert calculate_simple_v2("1 + 2 * 3 + 4 * 5 + 6".split()) == 231

parsed_lines_2 = list(calculate_nested(line=line, calculate_simple_fn=calculate_simple_v2) for line in lines)
result_2 = sum(parsed_lines_2)

print(f"Sum of results = {result_2}")

assert result_2 == 276894767062189