import re
from pprint import pprint
from functools import reduce
from copy import deepcopy

lines = open("./day20/input.txt").read().splitlines()[:-1]
# print(lines)

p_tile = re.compile("Tile (\d+):")

def find_edges(entries):
    yield entries[0]
    yield entries[-1]
    yield "".join(list(entry[0] for entry in entries))
    yield "".join(list(entry[-1] for entry in entries))

def parse_tiles(lines):
    tile = { 'entries': [] }
    for line in lines:
        if not line:
            tile['edges'] = list(find_edges(tile['entries']))
            yield tile
            tile = { 'entries': [] }
            continue
        match = p_tile.search(line)
        if match:
            tile['index'] = match.group(1)
        else:
            tile['entries'].append(line)

    tile['edges'] = list(find_edges(tile['entries']))
    yield tile

tiles = list(parse_tiles(lines))    
print(f"Number of tiles {len(tiles)}")

def build_adjacent_edges_map(tiles):
    result = {}
    for tile in tiles:
        for edge in tile['edges']:
            if edge not in result:
                result[edge] = set()
            result[edge].add(tile['index'])

            reverted_edge = edge[::-1]
            if reverted_edge not in result:
                result[reverted_edge] = set()
            result[reverted_edge].add(tile['index'])

    return result

edges_map = build_adjacent_edges_map(tiles)
# pprint(edges_map)

def calculate_adjacent_tiles(tiles, edges_map):
    adjs_map = {}
    for tile in tiles:
        adjs = []
        for edge in tile['edges']:
            for neighbour in edges_map[edge]:
                if neighbour != tile['index']:
                    adjs.append(neighbour)            
        adjs_map[tile['index']] = adjs
    return adjs_map        

adjacent_map = calculate_adjacent_tiles(tiles=tiles, edges_map=edges_map)
corner_indexes = list(int(key) for key,entry in adjacent_map.items() if len(entry) == 2)
print(f"Corner indexes {corner_indexes}")
answer_1 = reduce(lambda x,y: x*y, corner_indexes)
print(f"Anwer 1 = {answer_1}")

assert answer_1 == 140656720229539


print("==== Part 2 ====")

tiles_map = { tile['index']: tile for tile in tiles }

def rotate(original):
    return zip(*original[::-1])

def rotate_tile(tile):
    new_entries = list("".join(e) for e in rotate(tile['entries']))
    return {
        'index': tile['index'],
        'entries': new_entries,
        'edges': list(find_edges(new_entries))
    }

def reflect_tile(tile):
    new_entries = list("".join(e[::-1]) for e in tile['entries'])
    return {
        'index': tile['index'],
        'entries': new_entries,
        'edges': list(find_edges(new_entries))
    }

def describe_tile(d_tile, adjacent_map, edges_map):
    print(f"Describing tile {d_tile['index']} {d_tile['edges']}")
    for edge in d_tile['edges']:
        e = edges_map[edge]
        print(f"Edge {edge} - from map {e}")

    neighbours = adjacent_map[d_tile['index']]
    print(f"Neighbours {neighbours}")

# edges: 0 - top, 1 - bottom, 2 - left, 3 - right
def get_neightbour(tile, edges_map, index):
    edge = tile['edges'][index]
    adj = edges_map[edge]
    return next((e for e in adj if e != tile['index']), None)

def get_left_neighbour(tile, edges_map):
    return get_neightbour(tile, edges_map, 2)

def get_right_neightbour(tile, edges_map):
    return get_neightbour(tile, edges_map, 3)

def get_bottom_neighbour(tile, edges_map):
    return get_neightbour(tile, edges_map, 1)

def get_upper_neighbour(tile, edges_map):
    return get_neightbour(tile, edges_map, 0)

def normalize_first_line(top_left, tiles_map, edges_map):
    prev_tile_key = top_left
    indexes = [prev_tile_key]    
    current_tile_key = get_right_neightbour(tiles_map[prev_tile_key] , edges_map)    
    while current_tile_key:
        counter = 0
        while get_left_neighbour(tiles_map[current_tile_key], edges_map) != prev_tile_key or get_upper_neighbour(tiles_map[current_tile_key], edges_map):
            if counter == 4:
                tiles_map[current_tile_key] = reflect_tile(tiles_map[current_tile_key])
                counter = 0
            else:
                tiles_map[current_tile_key] = rotate_tile(tiles_map[current_tile_key])            
                counter += 1
        indexes.append(current_tile_key)      
        prev_tile_key = current_tile_key
        current_tile_key = get_right_neightbour(tiles_map[current_tile_key], edges_map)        
    return indexes

def normalize_first_column(top_left, tiles_map, edges_map):
    prev_tile_key = top_left
    indexes = [prev_tile_key]
    current_tile_key = get_bottom_neighbour(tiles_map[prev_tile_key] , edges_map)
    while current_tile_key:
        counter = 0
        while get_upper_neighbour(tiles_map[current_tile_key], edges_map) != prev_tile_key or get_left_neighbour(tiles_map[current_tile_key], edges_map):
            if counter == 4:
                tiles_map[current_tile_key] = reflect_tile(tiles_map[current_tile_key])
                counter = 0
            else:
                tiles_map[current_tile_key] = rotate_tile(tiles_map[current_tile_key])
                counter += 1
        indexes.append(current_tile_key)
        prev_tile_key = current_tile_key
        current_tile_key = get_bottom_neighbour(tiles_map[current_tile_key], edges_map)
    return indexes

def normalize_line(prev_tile_key, tiles_map, edges_map, upper_line_indexes):
    indexes = [prev_tile_key]    
    current_tile_key = get_right_neightbour(tiles_map[prev_tile_key] , edges_map)    
    while current_tile_key:
        counter = 0
        while get_left_neighbour(tiles_map[current_tile_key], edges_map) != prev_tile_key or get_upper_neighbour(tiles_map[current_tile_key], edges_map) not in upper_line_indexes:
            if counter == 4:
                tiles_map[current_tile_key] = reflect_tile(tiles_map[current_tile_key])
                counter = 0
            else:
                tiles_map[current_tile_key] = rotate_tile(tiles_map[current_tile_key])            
                counter += 1
        indexes.append(current_tile_key)      
        prev_tile_key = current_tile_key
        current_tile_key = get_right_neightbour(tiles_map[current_tile_key], edges_map)        
    return indexes

def normalize_tiles(top_left, tiles_map, edges_map):  
    start_indexes = normalize_first_column(top_left, tiles_map, edges_map)  
    # pprint(start_indexes)
    
    print(f"Working with line {top_left}")
    upper_line_indexes = normalize_first_line(top_left, tiles_map, edges_map)
    row_indexes = [upper_line_indexes]        
    for start_index in start_indexes[1:]:
        # print(f"Working with line {start_index}")
        current_line_indexes = normalize_line(start_index, tiles_map, edges_map, upper_line_indexes)
        upper_line_indexes = current_line_indexes
        row_indexes.append(current_line_indexes)

    # pprint(row_indexes)          
    return row_indexes

tiles_map['3221'] = rotate_tile(rotate_tile(tiles_map['3221']))
describe_tile(d_tile=tiles_map['3221'], adjacent_map=adjacent_map, edges_map=edges_map)
row_indexes = normalize_tiles(top_left='3221', tiles_map=tiles_map, edges_map=edges_map)
       
def print_raw_indexes(idx):
    for e in idx:
        print(e)            

print("After tiles normalized:")
print_raw_indexes(row_indexes)

# ['3221', '3313', '1451', '2143', '1283', '3803', '3989', '2267', '1453', '3413', '2609', '3343']
# ['3169', '1999', '1777', '2887', '1579', '3373', '1447', '1229', '2437', '1031', '3529', '2719']
# ['3659', '2381', '1907', '3581', '3677', '3527', '2017', '2521', '1483', '1097', '1511', '1223']
# ['3517', '1753', '2557', '1303', '2647', '2729', '3329', '2711', '2551', '3391', '1091', '2153']
# ['1129', '3923', '1051', '3019', '3613', '2383', '1459', '1297', '2843', '1367', '2953', '2617']
# ['1789', '2477', '1697', '1867', '2029', '2371', '1801', '2309', '2957', '2549', '3301', '2081']
# ['3779', '2593', '1213', '2339', '2803', '1109', '2293', '2851', '2129', '3467', '2693', '2837']
# ['1733', '1471', '3719', '2879', '3457', '1493', '1093', '2749', '2137', '3257', '2657', '2927']
# ['1663', '1019', '2131', '1277', '3557', '2621', '1847', '3919', '1429', '1621', '2347', '1823']
# ['2243', '2423', '1669', '3943', '3559', '3217', '3739', '2179', '1997', '3469', '2239', '1009']
# ['2203', '3727', '2897', '2819', '3511', '3299', '2039', '3617', '1201', '3701', '2687', '1913']
# ['3323', '3499', '3709', '1931', '2999', '2539', '3881', '1123', '1321', '2833', '2251', '3931']

tiles_map_clean = deepcopy(tiles_map)
for index_row,row in enumerate(row_indexes):
    for index_column,tile_key in enumerate(row):
        tiles_map_clean[tile_key]['entries'] = tiles_map_clean[tile_key]['entries'][:-1]
        tiles_map_clean[tile_key]['entries'] = tiles_map_clean[tile_key]['entries'][1:]
        tiles_map_clean[tile_key]['entries'] = list("".join(e[:-1]) for e in tiles_map_clean[tile_key]['entries'])
        tiles_map_clean[tile_key]['entries'] = list("".join(e[1:]) for e in tiles_map_clean[tile_key]['entries'])          
     
def prepare_puzzle(tm, row_indexes):
    puzzle = []
    for row in row_indexes:        
        row_entries = list(zip(*(tm[e]['entries'] for e in row)))
        result_entries = list("".join(e) for e in row_entries)
        puzzle += result_entries
    return puzzle
            
result_puzzle = prepare_puzzle(tiles_map_clean, row_indexes)

def print_puzzle(puzzle):
    for row in puzzle:
        print(row)

print("Puzzle after cleanup")
print_puzzle(result_puzzle)

def is_a_monster(lines):
    assert len(lines) == 3
    assert len(lines[0]) == len(lines[1]) == len(lines[2]) == 20
    if lines[0][18] != '#':
        return False
    if next((lines[1][e] for e in [0,5,6,11,12,17,18,19] if lines[1][e] != '#'), False):
        return False
    if next((lines[2][e] for e in [1,4,7,10,13,16] if lines[2][e] != '#'), False):
        return False
    return True        

sample_monster = """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   \
"""
assert is_a_monster(sample_monster.splitlines())

def rotate_puzzle(puzzle):
    return list("".join(e) for e in rotate(puzzle))

def reflect_puzzle(puzzle):
    return list("".join(e[::-1]) for e in puzzle)

def find_monsters(puzzle):
    counter = 0
    for i in range(len(puzzle)-2):
        for j in range(len(puzzle[i])-19):
            checking = [puzzle[i][j:j+20], puzzle[i+1][j:j+20], puzzle[i+2][j:j+20]]
            if is_a_monster(checking):
                counter += 1
    return counter

proper_orientated_puzzle = rotate_puzzle(rotate_puzzle(reflect_puzzle(result_puzzle)))
number_of_monsters = find_monsters(proper_orientated_puzzle)

print(f"Got {number_of_monsters} monsters!")

sharps_in_monster = 15 
overall = sum(e.count('#') for e in proper_orientated_puzzle)
answer_2 = overall - (sharps_in_monster * number_of_monsters)

print(f"Answer = {answer_2}")

assert answer_2 == 1885