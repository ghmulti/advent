import itertools

lines = open("./day6/input.txt").read()

groups = lines.split("\n\n")
group_answers = list(group.split() for group in groups)
# print(group_answers[:1])
group_answers_unique = list(set(itertools.chain.from_iterable(answers)) for answers in group_answers)
# print(group_answers_unique[:1])

#### part 1
group_answers_unique_count = sum(len(answers) for answers in group_answers_unique)
print(f"Sum of the unique answered questions count per group {group_answers_unique_count}")

#### part 2
def answered_by_all(group_answer, answer):
    return next((False for person_answer in group_answer if answer not in person_answer), True)

assert answered_by_all(["abc", "cde", "cfg"], "c") == True
assert answered_by_all(["abc", "def"], "a") == False

counter = 0
for (group_answer, group_answer_unique) in zip(group_answers, group_answers_unique):
    # print(f"Checking group {group_answer} with unique answers {group_answer_unique}")
    group_answer_by_all = list(answer for answer in group_answer_unique if answered_by_all(group_answer, answer))
    # print(f"{group_answer_by_all} found for every answer in {group_answer}")
    counter += len(group_answer_by_all)
print(f"Sum of count of questions answered by all in group {counter}")
