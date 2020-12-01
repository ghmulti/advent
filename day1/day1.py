
from itertools import combinations, islice
from functools import reduce 

day1_lines = open("./day1/input.txt")
lines = day1_lines.readlines()

def conv(lst):
    for e in lst:
        yield int(e.strip())

def calc(lines, amount):
    mapped_lines = combinations(conv(lines), amount)
    return (entry for entry in mapped_lines if sum(entry) == 2020)
    
###### part 1
passed_2 = next(calc(lines, 2))
print(passed_2, reduce(lambda x,y: x * y, passed_2))

###### part 2
passed_3 = next(calc(lines, 3))
print(passed_3, reduce(lambda x,y: x * y, passed_3))
