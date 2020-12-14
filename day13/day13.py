
from pprint import pprint

lines = open('day13/input.txt').read().splitlines()

print("==== Part 1 ====")

earliest_timestamp = int(lines[0])
buses_in_service  = list(int(l) for l in lines[1].split(",") if l != 'x')
print(f"{earliest_timestamp} - {buses_in_service}")

def build(buses):
    for bus_interval in buses:
        last_departure = earliest_timestamp % bus_interval
        diff = earliest_timestamp - last_departure + bus_interval
        time_to_wait = diff - earliest_timestamp
        yield [bus_interval, diff, bus_interval * time_to_wait]

departures = list(build(buses_in_service))
earliest_departure = min(r[1] for r in departures)
result_bus, result_diff, result_answer = next((departure for departure in departures if departure[1] == earliest_departure))
print(f"Result bus {result_bus}: diff {result_diff} = {result_answer}")    

assert 3464 == result_answer

print("==== Part 2 ====")

buses_with_indexes = list((offset, int(bus_id)) for offset, bus_id in enumerate(lines[1].split(",")) if bus_id != 'x')
print(buses_with_indexes)

def calculate_result_time(buses):
    result_time = 0
    step = 1
    for offset, bus_id in buses:
        # print(f"Wokring with bus {bus_id}, offset {offset}")
        while (result_time + offset) % bus_id != 0:
            result_time += step    
        step *= bus_id
        # print(f"Movint to step {step}")
        yield [result_time, step, bus_id]

timestamps = list(calculate_result_time(buses_with_indexes))
pprint(timestamps)
print(f"Result {timestamps[-1][0]}")