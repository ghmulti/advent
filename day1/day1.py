
from itertools import combinations, islice
from functools import reduce 
import operator

day1_lines = open("./day1/input.txt")
lines = day1_lines.readlines()

def calc(lines, amount):
    mapped_lines = combinations(map(int, lines), amount)
    return (entry for entry in mapped_lines if sum(entry) == 2020)
    
###### part 1
passed_2 = next(calc(lines, 2))
print(passed_2, reduce(operator.mul, passed_2))

###### part 2
passed_3 = next(calc(lines, 3))
print(passed_3, reduce(operator.mul, passed_3))
