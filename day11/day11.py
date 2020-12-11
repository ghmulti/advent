from pprint import pprint
from copy import deepcopy

lines = open("./day11/input.txt").read().split("\n")
filled_lines = list(line for line in lines if line)
# pprint(filled_lines)

def build_matrix(lines):
    for line in lines:
        yield [l for l in line]        

matrix = list(build_matrix(filled_lines))

def occupied_seats(mtx):
    for i in range(len(mtx)):
        for j in range(len(mtx[i])):
            if mtx[i][j] == '#':
                yield mtx[i][j]


def number_of_occupied_seats(mtx):
    occupied = occupied_seats(mtx)
    return len(list(occupied))

def build_occupy_seats_func(adjacent_search_fn, threshold):
    def func(mtx):
        newmtx = deepcopy(mtx)
        for row in range(len(mtx)):
            for col in range(len(mtx[row])):
                if newmtx[row][col] == '.':
                    continue
                else:
                    adj = list(adjacent_search_fn(mtx, row, col))
                    occupied_seats = number_of_occupied_seats([adj])
                    if mtx[row][col] == 'L' and occupied_seats == 0:
                        newmtx[row][col] = '#'
                    elif mtx[row][col] == '#' and occupied_seats >= threshold:
                        newmtx[row][col] = 'L'                            
        return newmtx
    return func


print("==== Part1 ====")

def adjacent_seats_v1(mtx, row, col):
    for i in range(row-1, row+2):
        for j in range(col-1, col+2):            
            if i < 0 or j < 0 or i >= len(mtx) or j >= len(mtx[i]):
                continue     
            if i == row and j == col:
                continue
            yield mtx[i][j]            

sample_adj = list(adjacent_seats_v1([[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]], 1, 1))
assert sample_adj == [1, 2, 3, 5, 7, 9, 10, 11]


occupy_seats_v1_fnc = build_occupy_seats_func(adjacent_search_fn=adjacent_seats_v1, threshold=4)
all_occupied_matrix = occupy_seats_v1_fnc(matrix)

current_matrix = matrix
newmatrix = all_occupied_matrix
while newmatrix != current_matrix:
    current_matrix = newmatrix
    newmatrix = occupy_seats_v1_fnc(newmatrix)    

current_occupied_seats = list(occupied_seats(current_matrix))
# print(current_occupied_seats)
number_of_occupied_seats_v1 = len(current_occupied_seats)
print(f"Number of occupied seats after hassle v1 {number_of_occupied_seats_v1}")

assert number_of_occupied_seats_v1 == 2424

print("==== Part 2 ====")

def direction(mtx, row, col, next_step, name):
    new_row, new_col = next_step(row, col)
    while True:
        if new_row < 0 or new_col < 0 or new_row >= len(mtx) or new_col >= len(mtx[0]):
            return None
        if mtx[new_row][new_col] == '.':
            new_row, new_col = next_step(new_row, new_col)
        else:            
            return mtx[new_row][new_col]

def adjacent_seats_v2(mtx, row, col):
    top = direction(mtx, row, col, lambda x,y: [x-1, y], 'top')
    bottom = direction(mtx, row, col, lambda x,y: [x+1, y], 'bottom')
    left = direction(mtx, row, col, lambda x,y: [x, y-1], 'left')
    right = direction(mtx, row, col, lambda x,y: [x, y+1], 'right')
    top_right = direction(mtx, row, col, lambda x,y: [x-1, y+1], 'top_right')
    bottom_right = direction(mtx, row, col, lambda x,y: [x+1, y+1], 'bottom_right')
    top_left = direction(mtx, row, col, lambda x,y: [x-1, y-1], 'top_left')
    bottom_left = direction(mtx, row, col, lambda x,y: [x+1, y-1], 'bottom_left')
    yield from [top, bottom, left, right, top_right, bottom_right, top_left, bottom_left]

v2_sample_mtx = [
    ['#', '.', '#', '#', '.', '#', '#', '.', '#', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '.', '#', '#']
]
v2_sample_adj = adjacent_seats_v2(v2_sample_mtx, 0, 2)
assert list(v2_sample_adj) == [None, '#', '#', '#', None, '#', None, '#']

occupy_seats_v2_fnc = build_occupy_seats_func(adjacent_search_fn=adjacent_seats_v2, threshold=5)

current_matrix_v2 = matrix
newmatrix_v2 = all_occupied_matrix
while newmatrix_v2 != current_matrix_v2:
    current_matrix_v2 = newmatrix_v2
    newmatrix_v2 = occupy_seats_v2_fnc(newmatrix_v2)
    
current_occupied_seats_2 = list(occupied_seats(current_matrix_v2))
# print(current_occupied_seats_2)
number_of_occupied_seats_v2 = len(current_occupied_seats_2)
print(f"Number of occupied seats after hassle v2 {number_of_occupied_seats_v2}")

assert number_of_occupied_seats_v2 == 2208