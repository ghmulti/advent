from itertools import combinations, product

# lines = open("./day17/input_test.txt").read().splitlines()
lines = open("./day17/input.txt").read().splitlines()

def neightbours(position, dimension):
    products = list(product((-1,0,1), repeat=dimension))
    for prod in products:
        val = list(map(sum, zip(prod, position)))
        if val == position:
            continue
        yield val

assert len(list(neightbours([0,0,0], 3))) == 26
assert len(list(neightbours([0,0,0,0], 4))) == 80

def build_cycles(n):
    start = [0]
    for _ in range(n):
        start = [start[0]-1] + start + [start[-1]+1]
        yield start

cycles = list(build_cycles(6))
assert cycles[-1] == [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]

print("==== Part 1 ====")

actives = {}
for x,line in enumerate(lines):
    for y,val in enumerate(line):
        if val == '#':
            actives[(x,y,0)] = 1

def find_actives(cycle, current_actives):
    target_actives = {}
    for x in range(-15,15):
        for y in range(-15,15):
            for z in cycle:
                nbs = list(neightbours([x,y,z],3))        
                active_nbs = list(1 for (nb_x,nb_y,nb_z) in nbs if current_actives.get((nb_x,nb_y,nb_z)))
                val = current_actives.get((x,y,z))
                # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
                # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
                if val and len(active_nbs) in [2,3]:
                    target_actives[(x,y,z)] = 1
                if not val and len(active_nbs) == 3:
                    target_actives[(x,y,z)] = 1
    return target_actives

new_actives = actives
print(f"Before any cycle, actives {len(new_actives)}")
for cycle in cycles:
    new_actives = find_actives(cycle, new_actives)
    print(f"Cycle {cycle}, actives {len(new_actives)}")

assert len(new_actives) == 293

print("==== Part 2 ====")

actives_v2 = {}
for x,line in enumerate(lines):
    for y,val in enumerate(line):
        if val == '#':
            actives_v2[(x,y,0,0)] = 1

def find_actives_v2(cycle, current_actives):
    target_actives = {}
    for x in range(-15,15):
        for y in range(-15,15):
            for w in range(-15,15):
                for z in cycle:
                    nbs = list(neightbours([x,y,z,w],4))        
                    active_nbs = list(1 for (nb_x,nb_y,nb_z,nb_w) in nbs if current_actives.get((nb_x,nb_y,nb_z,nb_w)))
                    val = current_actives.get((x,y,z,w))
                    # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
                    # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
                    if val and len(active_nbs) in [2,3]:
                        target_actives[(x,y,z,w)] = 1
                    if not val and len(active_nbs) == 3:
                        target_actives[(x,y,z,w)] = 1
    return target_actives

new_actives_v2 = actives_v2
print(f"Before any cycle, actives {len(new_actives_v2)}")
for cycle in cycles:
    new_actives_v2 = find_actives_v2(cycle, new_actives_v2)
    print(f"Cycle {cycle}, actives {len(new_actives_v2)}")    

assert len(new_actives_v2) == 1816