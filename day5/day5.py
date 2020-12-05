
lines = open("./day5/input.txt").readlines()
# print(lines)

def calculate_position(line):
    pos = [0, 127]
    for i in range(7):
        letter = line[i]
        diff = (pos[1] - pos[0] + 1)//2
        if letter == "F":
            pos = [pos[0], pos[1]-diff]
        else:
            pos = [pos[0]+diff, pos[1]]
        # print(pos)
    assert pos[0] == pos[1]

    pos2 = [0, 7]
    for i in range(3):
        letter = line[i + 7]
        diff = (pos2[1] - pos2[0] + 1)//2
        if letter == "L":
            pos2 = [pos2[0], pos2[1]-diff]
        else:
            pos2 = [pos2[0]+diff, pos2[1]]
        # print(pos2)
    assert pos2[0] == pos2[1]            

    return [pos[0],pos2[0]]

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

def all_positions():
    for row in range(128):
        if row <= 9 or row >= 116:
            continue
        for col in range(8):
            yield [row, col]

all_positions = list(all_positions())
free_positions = list(position for position in all_positions if position not in occupied_positions)
print(free_positions)
# print(len(free_positions))

free_seat_ids = list(seat_id(free_position) for free_position in free_positions)
# print(free_seat_ids)

free_seat_ids_filtered = list(free_seat_id for free_seat_id in free_seat_ids if free_seat_id+1 in occupied_seat_ids and free_seat_id-1 in occupied_seat_ids)
print(free_seat_ids_filtered)