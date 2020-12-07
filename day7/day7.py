import re

lines = open("./day7/input.txt").read()

groups = lines.split("\n")
# print(groups[:1])

src_p = re.compile("([\w\s]+) bag")
target_p = re.compile("(\d+) ([\w\s]+) bag")

bags = {}
for group in groups:
    subgroup = group.split("contain")

    source_match = src_p.search(subgroup[0])
    if source_match:
        src_group = source_match.group(1)
    else:
        continue

    # print(f"Subgroup {subgroup}")
    # print(f"Source color: [{src_group}]")

    target_subgroups = subgroup[1].split(",")
    bags_children = []
    for target_subgroup in target_subgroups:
        # print(target_subgroup)
        target_match = target_p.search(target_subgroup)
        if target_match:
            target_number = target_match.group(1)
            target_group = target_match.group(2)
            # print(f"Target group for {src_group}: {target_group}")            
            bags_children.append([target_group, int(target_number)])

    bags[src_group] = bags_children

# print(bags)

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