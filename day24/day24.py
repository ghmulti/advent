from pprint import pprint

lines = open("./day24/input.txt").read().splitlines()
# print(lines[-1])

ddirs = ["se", "sw", "nw", "ne"]

floor = {}

dd = {
    'e': (1, 0),
    'se': (1, 1),
    'sw': (0, 1),
    'w': (-1, 0),
    'nw': (-1, -1),
    'ne': (0, -1) 
}

def parse_direction(direct, pos):
    x, y = pos
    diffx, diffy = dd[direct]
    return (x+diffx,y+diffy)
    
print("==== Part 1 ====")

def process_line(line):
    newline = line[:]
    position = (0, 0)
    while len(newline) > 0:
        if any((dd for dd in ddirs if newline.startswith(dd))):
            position = parse_direction(newline[:2], position)
            newline = "".join(newline[2:])
        else:
            position = parse_direction(newline[:1], position)
            newline = "".join(newline[1:])
    return position

for line in lines:
    target_position = process_line(line)
    if target_position not in floor:
        floor[target_position] = 0
    floor[target_position] += 1

counter = 0
for key,entry in floor.items():
    if entry % 2 != 0:
        counter += 1


# pprint(floor)

print(f"Answer = {counter} [of {len(lines)}, {len(floor)}]")

assert counter == 400
