from pprint import pprint

lines = open("./day12/input.txt").read().split("\n")
filled_lines = list([line[0], int(line[1:])] for line in lines if line)
# print(filled_lines)

print("==== Part 1 ====")
ship_position_1 = {"E": 0, "W": 0, "S": 0, "N": 0}
directions = {0: "E", 90: "S", 180: "W", 270: "N"}

degrees_1 = 0
for instruction, value in filled_lines:
    if instruction in ["N", "S", "W", "E"]:
        ship_position_1[instruction] += value        
    elif instruction == "F":
        direction = directions[degrees_1]
        ship_position_1[direction] += value
    elif instruction in ["L", "R"]:
        degrees_1 = (degrees_1 + value * (-1, 1)[instruction == "R"]) % 360
        assert abs(degrees_1) in [0, 90, 180, 270]
    else:
        assert False, f"Invalid instruction {instruction}"

ns = abs(ship_position_1["N"] - ship_position_1["S"])
we = abs(ship_position_1["E"] - ship_position_1["W"])
distance_1 = ns + we
print(f"Result ship position {ship_position_1}, manhattan distance {distance_1}")   

assert ns == 1099
assert we == 397
assert ns + we == 1496

print("==== Part 2 ====")

waypoint_2 = [10, 1]
ship_position_2 = [0, 0]

angle_multiplier_map = {0: 1, 90: 1, 180: -1, 270: -1}

def rotate_v2(waypoint, direction, angle):
    assert angle in [0, 90, 180, 270]
    x, y = waypoint
    angle_multiplier = angle_multiplier_map[angle]
    if angle in [0, 180]:        
        return [x * angle_multiplier, y * angle_multiplier]
    else:
        direction_multiplier = (-1, 1)[direction == "R"]
        return [y * direction_multiplier * angle_multiplier, x * direction_multiplier * -angle_multiplier]
    
for instruction, value in filled_lines:
    if instruction in ["N", "S", "W", "E"]:
        x, y = waypoint_2
        diff_x = value*(-1, 1)[instruction == "E"] if instruction in ("E", "W") else 0
        diff_y = value*(-1, 1)[instruction == "N"] if instruction in ("N", "S") else 0
        waypoint_2 = [x + diff_x, y + diff_y]    
    elif instruction == "F":
        x, y = waypoint_2
        ship_x, ship_y = ship_position_2
        ship_position_2 = [ship_x + x*value, ship_y + y*value]
    elif instruction in ["L", "R"]:
        waypoint_2 = rotate_v2(waypoint_2, instruction, value)
    else:
        assert False, f"Invalid instruction {instruction}"

distance_2 = sum(map(abs, ship_position_2))
print(f"Result ship position {ship_position_2}, manhattan distance {distance_2}")        

assert ship_position_2 == [-6352, 57491]
assert distance_2 == 63843