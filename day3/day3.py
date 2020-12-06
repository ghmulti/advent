from itertools import islice, repeat
from functools import reduce
import operator

lines = open("./day3/input.txt").readlines()
# print(list(lines))

def hops(padding_x):
    start = 0
    while True:
        yield start
        start = start + padding_x

def objs(line, hop):
    md = hop % len(line)
    # print(md)
    return line[md]
    

def number_of_trees(padding_x, padding_y):
    line_num = 0
    hops_gen = hops(padding_x)
    objects = []
    while line_num < len(lines):
        objects.append(objs(lines[line_num].strip(), next(hops_gen)))
        line_num += padding_y
    # print(objects)
    trees = list(obj for obj in objects if obj == '#')
    return len(trees)

#### part 1
trees_3_1 = number_of_trees(3,1)
print(f"3,1={trees_3_1}")

#### part 2
trees_1_1 = number_of_trees(1,1)
print(f"1,1={trees_1_1}")
trees_5_1 = number_of_trees(5,1)
print(f"5,1={trees_5_1}")
trees_7_1 = number_of_trees(7,1)
print(f"7,1={trees_7_1}")
trees_1_2 = number_of_trees(1,2)
print(f"1,2={trees_1_2}")

result = reduce(operator.mul, [trees_1_1, trees_3_1, trees_5_1, trees_7_1, trees_1_2])
print(result)