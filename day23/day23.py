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

class Node:
    def __init__(self, value):
        self.next = self.prev = None
        self.value = value

class LinkedListWithCache:
    def __init__(self, values):
        self.cache = {}
        head = prev = None
        for value in values:
            node = Node(value)
            if not head:
                head = node
            if prev:
                prev.next = node
                node.prev = prev
            self.cache[value] = prev = node
        head.prev = prev
        prev.next = head
    
    def get(self, key):
        return self.cache[key]

    def move(self, source, dest):
        item, destination = self.cache[source], self.cache[dest]
        prev_next = destination.next
        item.prev.next = item.next
        item.next.prev = item.prev
        destination.next.prev = item
        destination.next = item
        item.prev = destination
        item.next = prev_next

def select_destination_wrapper(lowest, highest):
    def fn(pick, current_cup):
        return select_destination(pick, current_cup, lowest, highest)
    return fn

def run(cups, limit, steps):
    print(f"Working with {cups}")
    next_key = cups[0]
    cups = LinkedListWithCache(cups + list(range(max(cups) + 1, limit + 1)))
    current_step = 0
    select_destination_fn = select_destination_wrapper(1, limit)
    while current_step < steps:
        current_step += 1
        item = cups.get(next_key)
        tmp_next_key = item.next.next.next.next.value
        pick = [item.next.value, item.next.next.value, item.next.next.next.value]
        destination_value = select_destination_fn(pick, item.value)
        for p in pick[::-1]:
            cups.move(p, destination_value)
        next_key = tmp_next_key
    return cups

cups = list(int(e) for e in "739862541")
result = run(cups=cups, limit=1000000, steps=10000000)
index_one = result.get(1)
# print(f"Element 1 { index_one.next.value }")
# print(f"Element 2 { index_one.next.next.value }")

answer_2 = index_one.next.value * index_one.next.next.value

print(f"Answer = {answer_2}")

assert answer_2 == 3072905352
