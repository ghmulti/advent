from itertools import islice

numbers = [0,13,1,16,6,17]

def get_next_number(spoken, previous_number):
    if previous_number not in spoken or len(spoken[previous_number]) == 1:
        return 0
    else:
        return spoken[previous_number][-1] - spoken[previous_number][-2]

def counter(numbers):
    yield from numbers
    spoken = { v:[k] for k,v in enumerate(numbers) }
    counter = len(numbers)
    prev_number = numbers[-1]
    while True:    
        next_number = get_next_number(spoken, prev_number)
        yield next_number
        spoken[next_number] = [spoken[next_number][-1], counter] if next_number in spoken else [counter]
        prev_number = next_number
        counter += 1

print(numbers)

answer_1 = next(islice(counter(numbers), start=2020-1, stop=2020))
print(f"2020 element is {answer_1}")
assert answer_1 == 234

answer_2 = next(islice(counter(numbers), start=30000000-1, stop=30000000))
print(f"30000000 element is {answer_2}")
assert answer_2 == 8984