
lines = open("./day5/input.txt").readlines()
# print(lines)

def binary_search(power, line, lower_predicate):
    pos = [0, 2**power - 1]    
    for i in range(power):
        letter = line[i]
        diff = (pos[1] - pos[0] + 1)//2
        if lower_predicate(letter):
            pos = [pos[0], pos[1]-diff]
        else:
            pos = [pos[0]+diff, pos[1]]
        # print(pos)
    assert pos[0] == pos[1], (f"Not equals for line {line} for power {power}", pos[0], pos[1])
    return pos[0]

def calculate_position(line):
    row = binary_search(power=7, line=line[:7], lower_predicate=lambda letter: letter == "F")
    column = binary_search(power=3, line=line[7:], lower_predicate=lambda letter: letter == "L")
    return [row, column]

assert calculate_position("FBFBBFFRLR") ==  [44,5]
assert calculate_position("BFFFBBFRRR") ==  [70,7]
assert calculate_position("BBFFBBFRLL") ==  [102,4]

def seat_id(seat):
    return seat[0] * 8 + seat[1]

assert seat_id(calculate_position("FBFBBFFRLR")) == 357 

occupied_positions = list(calculate_position(line.strip()) for line in lines)
# print(occupied_positions)
occupied_seat_ids = list(seat_id(position) for position in occupied_positions)
# print(occupied_seat_ids)


#### part 1
max_occupied_seat_id = max(occupied_seat_ids)
print(f"Max occupied seat id {max_occupied_seat_id}")


#### part 2
def all_positions():
    for row in range(128):
        for col in range(8):
            yield [row, col]

free_positions = list(p for p in all_positions() if p not in occupied_positions)
# print(free_positions)
free_positions_filtered = list(p for p in free_positions if [p[0], p[1]+1] not in free_positions and [p[0], p[1]-1] not in free_positions)
# print(free_positions_filtered)

free_seat_ids = list(seat_id(free_position) for free_position in free_positions_filtered)
# print(free_seat_ids)
free_seat_ids_filtered = list(fsi for fsi in free_seat_ids if fsi+1 in occupied_seat_ids and fsi-1 in occupied_seat_ids)

assert len(free_seat_ids_filtered) == 1
print(f"Your seat id is {free_seat_ids_filtered[0]}")