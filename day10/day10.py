from functools import reduce

lines = open("./day10/input.txt").read().split("\n")

joltage = list(int(line) for line in lines if line)
joltage.sort()

def joltage_with_outlet(joltage):
    return [0] + joltage

def joltage_with_device(joltage):
    return joltage + [joltage[-1]+3]

#### part 1
def diff_count(joltages, diff):
    for key,j in enumerate(joltages):
        if key == 0:
            continue
        if j - joltages[key-1] == diff:
            yield [key, j]

joltage_1 = joltage_with_device(joltage_with_outlet(joltage))
one_diff = list(diff_count(joltage_1, 1))
three_diff = list(diff_count(joltage_1, 3))
answer = len(one_diff) * len(three_diff)
print(f"Result = {len(one_diff)} diff for 1 joltage,  {len(three_diff)} diff for 3 joltage; answer {answer}")

assert len(one_diff) == 66
assert len(three_diff) == 28
assert answer == 1848

#### part 2
def is_valid_list(joltage_with_outlet):
    for i in range(len(joltage_with_outlet) - 1):
        if joltage_with_outlet[i+1] - joltage_with_outlet[i] > 3:
            return False
    return True

def build_subgroups(joltage_with_outlet):
    group = []
    for k,v in enumerate(joltage_with_outlet):
        diff = v - joltage_with_outlet[k-1]
        if diff >= 3:
            yield group
            group = [v]
        else:
            group.append(v)
    yield group

def check_removable(source, ind, removables):    
    res = 1
    for k, removable in enumerate(removables):
        if k < ind:
            continue  
        # print(f"Checking removable {source} {removable}")
        new_src = source[::]
        new_src.remove(removable)
        is_valid = is_valid_list(new_src)
        if not is_valid:
            continue
        res += check_removable(new_src, k+1, removables)
    return res

def calculate_unique_combinations(source, subgroup):
    removables = subgroup[1:-1] 
    # print(f"Removable {removable}")
    return check_removable(source, 0, removables)

def number_of_combinations(sublists):
    return reduce(lambda x,y: x*y, sublists)


example_joltage = joltage_with_outlet([1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19])
assert is_valid_list(example_joltage)
assert not is_valid_list([1,5])
example_subgroups = list(build_subgroups(example_joltage))
assert example_subgroups == [[0, 1], [4, 5, 6, 7], [10, 11, 12], [15, 16], [19]]
example_unique_combinations = list(calculate_unique_combinations(source=example_joltage, subgroup=subgroup) for subgroup in example_subgroups)
assert [1, 4, 2, 1, 1] == example_unique_combinations
assert number_of_combinations(example_unique_combinations) == 8


joltage_2 = joltage_with_outlet(joltage)
subgroups_2 = list(build_subgroups(joltage_2))
combinations_2 = list(calculate_unique_combinations(source=joltage_2, subgroup=subgroup) for subgroup in subgroups_2)
unique_combinations = number_of_combinations(combinations_2)
print(f"{unique_combinations} unique combinations for all adapters found")

assert 8099130339328 == unique_combinations