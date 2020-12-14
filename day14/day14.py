from pprint import pprint
import re
from itertools import product

lines = open("./day14/input.txt").readlines()

src_p = re.compile("\[(\d+)\] = (\d+)")

def bits(number):
    return '{0:036b}'.format(number)

assert '000000000000000000000000000000001011' == bits(11), bits(11)
assert '000000000000000000000000000001100101' == bits(101), bits(101)

print("==== Part 1 ====")

def apply_mask(mask, value):
    bits_value = [v for v in bits(value)]
    return "".join((mask_bit, bits_value[index])[mask_bit == 'X'] for index, mask_bit in enumerate(mask))

sample = apply_mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 11)
assert sample == '000000000000000000000000000001001001', sample
assert int(sample, 2) == 73

sample2 = apply_mask('XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 101)
assert sample2 == '000000000000000000000000000001100101', sample2
assert int(sample2, 2) == 101

current_mask = None
memory_dump_1 = {}
for line in lines:
    if line.startswith('mask ='):
        current_mask = line[-37:-1]
        continue
    if line.startswith('mem'):
        matches = src_p.search(line)
        key = int(matches.group(1))
        value = int(matches.group(2))
        applied = apply_mask(current_mask, value)
        memory_dump_1[key] = int(applied, 2)

answer_1 = sum(memory_dump_1.values())
print(f"Answer v1 {answer_1}")

assert answer_1 == 12610010960049

print("==== Part 2 ====")

def apply_mask_v2(mask, value):
    bits_value = [v for v in bits(value)]
    return "".join((mask_bit, bits_value[index])[mask_bit == '0'] for index, mask_bit in enumerate(mask))

sample3 = apply_mask_v2('000000000000000000000000000000X1001X', 42)
assert sample3 == '000000000000000000000000000000X1101X', sample3

def value_combinations(value):
    value_list = ([index, bit] for index,bit in enumerate(value))
    xes = list(filter(lambda x: x[1] == "X", value_list))
    products = product([0,1], repeat = len(xes))
    for masked_values in products:
        list_copy = list(v for v in value)
        for key, xe in enumerate(xes):
            index, _ = xe
            list_copy[index] = str(masked_values[key])
        yield "".join(list_copy)

sample4 = '000000000000000000000000000000X1101X'
combs_sample = list(value_combinations(sample4))
assert len(combs_sample) == 4
assert '000000000000000000000000000000011010' in combs_sample, combs_sample
assert '000000000000000000000000000000011011' in combs_sample, combs_sample
assert '000000000000000000000000000000111010' in combs_sample, combs_sample
assert '000000000000000000000000000000111011' in combs_sample, combs_sample

current_mask_v2 = None
memory_dump_2 = {}
for line in lines:
    if line.startswith('mask ='):
        current_mask_v2 = line[-37:-1]
        continue
    if line.startswith('mem'):
        matches = src_p.search(line)
        default_key = int(matches.group(1))
        value = int(matches.group(2))
        target_mask = apply_mask_v2(current_mask_v2, default_key)
        target_combs = value_combinations(target_mask)
        for comb in target_combs:
            key = int(comb, 2)
            memory_dump_2[key] = value

answer_2 = sum(memory_dump_2.values())
print(f"Answer v2 {answer_2}")

assert answer_2 == 3608464522781