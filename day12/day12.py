from pprint import pprint

lines = open("./day12/input.txt").read().split("\n")
filled_lines = list(line for line in lines if line)
pprint(filled_lines)