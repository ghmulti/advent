import re
from pprint import pprint
from functools import reduce

lines = open("./day16/input.txt").read().splitlines()

rules_raw = lines[:20]
your_ticket = lines[22:23][0]
tickets_raw = lines[25:]

rules_p = re.compile("(.*): (\d+)-(\d+) or (\d+)-(\d+)")

def parse_rules(r):
    for ru in r:
        matches = rules_p.search(ru)
        yield {'name': matches.group(1), 'interval1': [int(matches.group(2)), int(matches.group(3))], 'interval2': [int(matches.group(4)), int(matches.group(5))]}

rules = list(parse_rules(rules_raw))
# pprint(rules)

def check_rule(rule, value):
    return (value >= rule['interval1'][0] and value <= rule['interval1'][1]) or (value >= rule['interval2'][0] and value <= rule['interval2'][1])

assert check_rule({'interval1': [1, 10], 'interval2': [50, 55]}, 3)
assert check_rule({'interval1': [1, 10], 'interval2': [50, 55]}, 55)
assert not check_rule({'interval1': [1, 10], 'interval2': [50, 55]}, 60)

print("==== Part 1 ====")

def invalid_fields(tickets, rules):
    for ticket_raw in tickets:
        vals = list(int(val) for val in ticket_raw.split(","))
        for val in vals:            
            passed_rule = next((rule for rule in rules if check_rule(rule, val)), None)
            if not passed_rule:                
                yield val
                

invalid_values = list(invalid_fields(tickets_raw, rules))    
answer_1 = sum(invalid_values)
print(f"Sum of invalid values = {answer_1}")

assert answer_1 == 20058

print("==== Part 2 ====")

def validate_ticket(ticket):
    vals = list(int(val) for val in ticket.split(","))
    for val in vals:            
        passed_rule = next((rule for rule in rules if check_rule(rule, val)), None)
        if not passed_rule:                
            return False
    return True

valid_tickets = list(ticket for ticket in tickets_raw if validate_ticket(ticket))            
print(f"Number of valid tickets {len(valid_tickets)}, total number of tickets {len(tickets_raw)}")

def passing_rules(values, rules):
    for rule in rules:
        mismatch_found = next((val for val in values if not check_rule(rule, val)), None)
        if not mismatch_found:
            yield rule['name']

sample_rules = [{'interval1': [1,2], 'interval2': [3,4], 'name':'sample'}, {'interval1': [1,3], 'interval2': [10,20], 'name': 'sample2'}]
sample_passing_rules = list(passing_rules([1,2,3,4], sample_rules))
assert sample_passing_rules == ['sample']

def cleanup(index_names):
    to_cleanup = list(e[0] for e in index_names if len(e) == 1)
    if len(index_names) == len(to_cleanup):
        return index_names
    else:        
        for index, e in enumerate(index_names):
            if len(e) > 1:
                index_names[index] = list(set(index_names[index]).difference(set(to_cleanup)))
        return cleanup(index_names)

def find_index_names(index_values, rules):
    index_names = list(list(passing_rules(index_value, rules)) for index_value in index_values)    
    cleaned_up_index_names = cleanup(index_names)
    return list(e[0] for e in cleaned_up_index_names)

def classify_fields(tickets, rules):
    index_values = list(zip(*(map(int, ticket.split(",")) for ticket in tickets)))    
    return find_index_names(index_values, rules)


index_names = classify_fields(valid_tickets, rules)
print(f"Index names are: {index_names}")

your_tiket_values = list(int(val) for val in your_ticket.split(","))
print(f"Your ticket: {your_ticket}")
your_ticket_mapped = { name:your_tiket_values[index] for index, name in enumerate(index_names) }
# pprint(your_ticket_mapped)

departure_values = list(your_ticket_mapped[key] for key in your_ticket_mapped if key.startswith('departure'))
print(f"Departure values = {departure_values}")
answer_2 = reduce(lambda x, y: x * y, departure_values)
print(f"Multiplication of departure values = {answer_2}")    

assert answer_2 == 366871907221