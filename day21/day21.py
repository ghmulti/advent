import re
from pprint import pprint
from itertools import chain

lines = open("./day21/input.txt").read().splitlines()
# print(lines[0])
# print(lines[-1])

p = re.compile('(.*) \(contains (.*)\)')

def parse_lines(lines):
    for line in lines:
        match = p.search(line)
        keys = list(key.strip() for key in match.group(2).split(','))
        values = list(match.group(1).split(' '))   
        yield keys,values

lines_p = list(parse_lines(lines))

def build_allergens_map(lines):
    for keys,values in lines:
        for key in keys:
            yield key,set(values)


allergens_map = list((k,v) for k,v in build_allergens_map(lines_p))
# pprint(allergens_map)

print("==== Part 1 ====")

def search_allergy_words(ingridient, parse_lines):
    result = None
    for key, value in parse_lines:
        if key != ingridient:
            continue
        if not result:
            result = value.copy()
        else:
            result = result.intersection(value)
    return result

allergens_keys = set(k for k,_ in allergens_map)
print(allergens_keys)

allergens_guess = {key: search_allergy_words(key, allergens_map) for key in allergens_keys}
# pprint(allergens_guess)

def cleanup(res):
    to_filter = set(next(iter(v)) for k,v in res.items() if len(v) == 1)
    # print(f"Cleaning up {to_filter}")
    if len(to_filter) == len(res):
        return res
    for k in res:
        if len(res[k]) == 1:
            continue
        res[k] = res[k].difference(to_filter)
    return cleanup(res)

allergens_guess_clean = {k:next(iter(v)) for k,v in cleanup(allergens_guess).items()}
# pprint(allergens_guess_clean)

allergens = set(allergens_guess_clean.values())
print(f"Found allergens: {allergens}")

no_allergens = set()
for _,ingredients in lines_p:
    no_allergens_step = set(ingredients).difference(allergens)
    no_allergens = no_allergens.union(no_allergens_step)

print(f"Total {len(no_allergens)} ingredients without allergies")

counter = 0
for _,ingredients in lines_p:
    for ingredient in ingredients:
        if ingredient in no_allergens:
            counter += 1

print(f"Answer 1 = {counter}")

assert counter == 2635

print("==== Part 2 ====")