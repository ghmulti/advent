import re
from pprint import pprint
from functools import reduce

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
print(f"Tile size 10x10")
# pprint(tiles[0])
# pprint(tiles[-1])

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

def rotate_entries(original):
    return zip(*original[::-1])

def rotate_tile(tile):
    new_entries = list("".join(e) for e in rotate_entries(tile['entries']))
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
    # for neighbour in neighbours:
    #     n_tile = tiles_map[neighbour]
    #     print(f"Neighbour {neighbour} {n_tile['edges']}")

# 3221  3313  1451  2143  1283  3803  3989  2267  1453 3413  2609  3343
# 3169  
# 3659
# 3517
# 1129
# 1789
# 3779
# 1733
# 1663
# 2243
# 2203
# 3323  3499  3709  1931  2999  2539  3881  1123  1321  2833  2251  3931

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

def normalize_tiles(top_left, tiles_map, adjacent_map, edges_map):  
    start_indexes = normalize_first_column(top_left, tiles_map, edges_map)  
    # pprint(start_indexes)
    
    print(f"Working with line {top_left}")
    upper_line_indexes = normalize_first_line(top_left, tiles_map, edges_map)
    row_indexes = [upper_line_indexes]        
    for start_index in start_indexes[1:]:
        print(f"Working with line {start_index}")
        current_line_indexes = normalize_line(start_index, tiles_map, edges_map, upper_line_indexes)
        upper_line_indexes = current_line_indexes
        row_indexes.append(current_line_indexes)

    # pprint(row_indexes)          

tiles_map['3221'] = rotate_tile(rotate_tile(tiles_map['3221']))
# describe_tile(d_tile=tiles_map['3221'], adjacent_map=adjacent_map, edges_map=edges_map)
normalize_tiles(top_left='3221', tiles_map=tiles_map, adjacent_map=adjacent_map, edges_map=edges_map)