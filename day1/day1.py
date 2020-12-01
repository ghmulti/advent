
from itertools import combinations, islice

day1_lines = open("./day1/input.txt")
lines = day1_lines.readlines()

def conv(lst):
    for e in lst:
        yield int(e.strip())


###### part 1
lines_comb_2 = combinations(lines, 2)
mapped_lines_2 = (list(conv(line)) for line in lines_comb_2)
passed_2 = ([entry, entry[0] * entry[1]] for entry in mapped_lines_2 if sum(entry) == 2020)
print(next(passed_2))

###### part 2
lines_comb_3 = combinations(lines, 3)
mapped_lines_3 = (list(conv(line)) for line in lines_comb_3)
passed_3 = ([entry, entry[0] * entry[1] * entry[2]] for entry in mapped_lines_3 if sum(entry) == 2020)
print(next(passed_3))
