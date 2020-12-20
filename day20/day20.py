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

# edges: 0 - top, 1 - bottom, 2 - left, 3 - right
# 3221**      3343
#  
# 
# 3931        3323

tiles_map['3221'] = rotate_tile(rotate_tile(tiles_map['3221']))

describe_tile(d_tile=tiles_map['3221'], adjacent_map=adjacent_map, edges_map=edges_map)
describe_tile(d_tile=tiles_map['3931'], adjacent_map=adjacent_map, edges_map=edges_map)
describe_tile(d_tile=tiles_map['3323'], adjacent_map=adjacent_map, edges_map=edges_map)
describe_tile(d_tile=tiles_map['3343'], adjacent_map=adjacent_map, edges_map=edges_map)
