from itertools import product, combinations

lines = open("./day19/input.txt").read().splitlines()

rules_raw = lines[:138]
# print(rules_raw[-1])

lines_raw = lines[139:]
# print(lines_raw)

def parse_rule(rule):
    parts_1 = rule.split(':')
    parts_2 = parts_1[1].split('|')
    v1 = list(e for e in parts_2[0].split()) if len(parts_2[0].split()) > 1 or parts_2[0].strip().isdigit() else parts_2[0].replace('"', '').strip()
    v2 = list(e for e in parts_2[1].split()) if len(parts_2) > 1 else []
    v = [v1,v2] if v1 and v2 else [v1]
    return (parts_1[0], v)

assert parse_rule("61: 84 72 | 71 58") == ('61', [['84', '72'], ['71', '58']])
assert parse_rule("130: 58 58") == ('130', [['58', '58']])
assert parse_rule('72: "a"') == ('72', ['a'])
assert parse_rule('117: 58') == ('117', [['58']])

parsed_rules = (parse_rule(rule_raw) for rule_raw in rules_raw)
rules_map = { k:v for k,v in parsed_rules }

def find_to_replace(rules):
    result = {}
    for key,value in rules.items():
        letters = list(v for v in value if isinstance(v, str))
        if len(letters) == len(value):
            result[key] = value
    return result

assert find_to_replace({'1': ['a'], '2': [['3']]}) == {'1': ['a']}

def do_replace(k, values, to_replace):
    # print(f"About to replace {k} {values}, {to_replace}")
    for val in values:
        # print(f"Woring with {val}")
        if set(val).difference(set(to_replace.keys())):
            yield val
            continue     
        combs = [to_replace[e] for e in val]
        yield from set("".join(e) for e in product(*combs))        

def iteration(rules, prev_to_replace_keys=-1, index=0):
    to_replace = find_to_replace(rules)
    if len(to_replace) == prev_to_replace_keys:        
        return rules
    
    new_map = to_replace.copy()
    for k,v in rules.items():
        if k in to_replace:
            continue
        new_map[k] = list(do_replace(k, v, to_replace))
    # print(f"Iteration new map {index}")    
    return iteration(new_map, len(to_replace), index+1)

print("==== Part 1 ====")

result = iteration(rules_map)
target_rule = set(result['0'])
print(f"Target rule {len(target_rule)}")

passed_messages_1 = list(e for e in lines_raw if e in target_rule)
answer_1 = len(passed_messages_1)
print(f"Answer 1 = {answer_1}")

assert answer_1 == 142

print("==== Part 2 ====")

def calculate_trailing_values(line, values, counter=(0,0)):
    found_last = next((value for value in values if line.endswith(value)), None)
    if found_last:
        return calculate_trailing_values(line[:-len(found_last)], values, (counter[0] + 1, counter[1] + len(found_last)))
    else:
        return counter

# 0: 8 11
# 8: 42     | 42 8          => 42++
# 11: 42 31 | 42 11 31      => (42,31)++
passed_messages_2 = []
for line in lines_raw:
  counter_31, length_31 = calculate_trailing_values(line=line, values=result['31'])
  if counter_31 == 0:
    continue
  sub_line = line[:-length_31]
  counter_41, length_41 = calculate_trailing_values(line=sub_line, values=result['42'])
  if length_41 == len(sub_line) and counter_41 > counter_31:
    passed_messages_2.append(line)

answer_2 = len(passed_messages_2)
print(f"Answer 2 = {answer_2}")

assert answer_2 == 294