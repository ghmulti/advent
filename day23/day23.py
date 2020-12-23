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
