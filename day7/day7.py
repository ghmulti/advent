import re
from functools import reduce

lines = open("./day7/input.txt").read()

groups = lines.split("\n")
# print(groups[:1])

src_p = re.compile("([\w\s]+) bag")
target_p = re.compile("(\d+) ([\w\s]+) bag")

def parse_line(acc: map, line: str):
    if not line:
        return acc
    [source_bag, target_bags_str] = line.split(" bags contain")
    target_bags_raw = target_bags_str.split(",")    
    target_bag_matches = (target_p.search(target_bag) for target_bag in target_bags_raw)
    acc[source_bag] = list([m.group(2), int(m.group(1))] for m in target_bag_matches if m)
    return acc

bags = reduce(parse_line, groups, {})

#### part 1

def search_parent(search_item):
    # print(f"Working with {search_item}")
    result = set()
    for src, children in bags.items():
        target_items = list(child[0] for child in children)
        if search_item in target_items:
            result.add(src) 
            result = result.union(search_parent(src))
    return result
        
bag_holders = search_parent("shiny gold")
# print(f"Bag holders {bag_holders}")
print(f"Number of bag holders {len(bag_holders)}")
# 179

#### part 2

def search_nested(search_item):    
    # print(f"Working with {search_item}")
    local_sum = 0
    for item in bags[search_item]:
        num = item[1]
        # print(f"Nested for {search_item}: {item}")
        local_sum += num + num * search_nested(item[0])
    return local_sum
 
total_sum = search_nested("shiny gold")
print(f"Result {total_sum}")
# 18925