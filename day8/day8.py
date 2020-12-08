from copy import deepcopy

lines = open("./day8/input.txt").read().split("\n")
# print(list(enumerate(lines)))

def line_parse(line):    
    return [line[0], line[1][:3], int(line[1][3:])]

lines_parsed = list(line_parse(line) for line in enumerate(lines) if line[1])
# print(lines_parsed[:1])

last_instruction = lines_parsed[-1:][0]
# print(f"Last instruction {last_instruction}")

def process(lns):
    index = 0
    visited = []    
    while True:
        if index >= len(lns):
            return

        yield lns[index]
        index, cmd, val = lns[index]        
        # print(f"Current line {index} {cmd} {val}, agg {acc}")
        if index in visited:
            break
        visited.append(index)
        if cmd == 'jmp':                
            index += val
        elif cmd == 'acc':
            index += 1
        elif cmd == 'nop':
            index += 1

#### part 1
res = list(process(lines_parsed))
print(f"Total steps {len(res)}, last step {res[-1:]}")
total_sum = sum(r[2] for r in res if r[1] == 'acc')
print(f"Total sum: {total_sum}")

assert total_sum == 1654

#### part 2
total_sum_x = -1
for x in res[::-1]:
    index, cmd, val = x
    # print(f"Working with index {index}")
    if cmd == 'nop':
        new_lines = deepcopy(lines_parsed)        
        new_lines[index][1] = 'jmp'
        res_x = list(process(new_lines))
    elif cmd == 'jmp':
        new_lines = deepcopy(lines_parsed)
        new_lines[index][1] = 'nop'
        res_x = list(process(new_lines))

    if res_x[-1][0] == last_instruction[0]:
        print(f"Faulty line [{index}, {cmd}, {val}]")
        print(f"Total steps {len(res_x)}, last strep {res_x[-1:]}")
        total_sum_x = sum(r[2] for r in res_x if r[1] == 'acc')
        print(f"Proper result after fix {total_sum_x}")    
        break

assert total_sum_x == 833