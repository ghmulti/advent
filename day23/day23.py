from itertools import islice
from pprint import pprint

print("==== Part 1 ====")

def select_destination(pick, current_cup, lowest, highest):
    while True:
        current_cup = current_cup - 1
        if current_cup < lowest:
            current_cup = highest        
        if current_cup not in pick:
            return current_cup
        
def move(cups):
    print(f"Working with {cups}")
    highest = max(cups)
    lowest = min(cups)

    current_index = 0
    while True:    
        # print(f"Cups {cups}")
        current_cup = cups[0]    
        # print(f"Current cup {current_cup}")
        pick = cups[1:4]
        # print(f"Picked {pick}")
        destination = select_destination(pick, current_cup, lowest, highest)
        destination_index = cups.index(destination)
    
        cups = cups[4:destination_index+1] + pick + cups[destination_index+1:] + [current_cup]
        yield cups
        current_index += 1

cups = list(int(e) for e in "739862541")
moves = list(islice(move(cups), 100))
target_move = moves[-1]

target_move_arranged = target_move[target_move.index(1)+1:] + target_move[:target_move.index(1)]
answer_1 = "".join((str(e) for e in target_move_arranged))
print(f"Answer = {answer_1}")

print("==== Part 2 ====")


# def select_destination(pick, current_cup, lowest, highest):
#     while True:
#         current_cup = current_cup - 1
#         if current_cup < lowest:
#             current_cup = highest        
#         if current_cup not in pick:
#             return current_cup

# def move(cups, limit, steps):
#     print(f"Working with {cups}")
#     source_cups = cups[::]
#     cups = cups + list(range(max(cups) + 1, limit + 1))
#     current_index = 0
#     current_step = 0
#     subindex_1 = []
#     subindex_2 = []
#     last_pick = None
#     last_el = None
#     current_index = 0       
#     while current_step < steps:
#         current_step += 1

#         if last_el and cups[current_index] - last_pick == 1:
#             subindex_1.append(cups[current_index])
#             subindex_2.append(cups[current_index+1])
#             subindex_2.append(cups[current_index+2])
#             subindex_2.append(cups[current_index+3])
#             last_pick = subindex_2[-1]
#             current_index += 4
#             continue
#         else:
#             if subindex_1:
#                 destination_index = select_destination(subindex_2, subindex_1[0], 1, limit)
#                 cups = cups[current_index:destination_index+1] + subindex_2 + cups[destination_index+1:] + subindex_1
#                 current_index = 0
#                 subindex_1 = []
#                 subindex_2 = []
#                 last_pick = None
#                 continue

#         current_cup = cups.pop(0)
#         pick = [cups.pop(0), cups.pop(0), cups.pop(0)]
#         last_pick = pick[-1]
#         last_el = current_cup
#         destination = select_destination(pick, current_cup, 1, limit)
#         destination_index = cups.index(destination)    
#         cups = cups[:destination_index+1] + pick + cups[destination_index+1:] + [current_cup]                    
#         print(f"[{current_step}] Current cup {current_cup}, pick {pick} {cups}")        

#     return cups

# cups = list(int(e) for e in "389125467")
# # result = move(cups=cups, limit=1000000, steps=10000000)
# result = move(cups=cups, limit=9, steps=10)
# print(result)
# index_one = result.index(1)
# print(f"Element 1 { result[index_one + 1] }")
# print(f"Element 2 { result[index_one + 2] }")