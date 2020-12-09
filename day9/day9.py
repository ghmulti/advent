from itertools import combinations

lines = open("./day9/input.txt").read().split("\n")
# print(lines)

numbers = list(int(n) for n in lines if n)
# print(numbers)

#### part 1
def search_invalid_numbers(nums, limit):
    for index,number in enumerate(nums[limit:]):
        prev_nums = nums[index:index+limit]
        comb_prev_nums = combinations(prev_nums, 2)
        comb_sum = (sum(e) for e in comb_prev_nums)
        result = any(e for e in comb_sum if e == number)
        if not result:
            yield [index, number]

invalid_number = next(search_invalid_numbers(nums=numbers, limit=25), None)
print(f"Invalid number {invalid_number}")
        
assert invalid_number[1] == 1398413738

#### part 2
def chunks(lst, n):
    for i in range(0, len(lst), 1):
        yield lst[i:i+n]

def check_chunks(lst, n, target_result):
    return (chunk for chunk in chunks(lst, n) if sum(chunk) == target_result)

for i in range(2, len(numbers), 1):
    result_chunk = next(check_chunks(numbers, i, invalid_number[1]), None)
    if result_chunk:
        max_n = max(result_chunk)
        min_n = min(result_chunk)
        print(f"Found result chunk {i}, max={max_n}, min={min_n}")
        
        assert max_n + min_n == 169521051        
        break
