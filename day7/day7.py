
lines = open("./day7/input.txt").read()

groups = lines.split("\n\n")
subgroups = list(group.split() for group in groups)