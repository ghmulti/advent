import itertools

lines = open("./day6/input.txt").read()

groups = lines.split("\n\n")
group_answers = list(group.split() for group in groups)
# print(group_answers[:1])
group_answers_unique = list(set(itertools.chain.from_iterable(answers)) for answers in group_answers)
# print(group_answers_unique[:1])
# print(group_answers_unique[-1:])

#### part 1
group_answers_unique_count = sum(len(answers) for answers in group_answers_unique)
print(f"Sum of the unique answered questions count per group {group_answers_unique_count}")

#### part 2
def answered_by_all(group_answer, answer):
    return next((False for person_answer in group_answer if answer not in person_answer), True)

assert answered_by_all(["abc", "cde", "cfg"], "c") == True
assert answered_by_all(["abc", "def"], "a") == False

def answers_answered_by_all(group_answer, answers):
    return set(answer for answer in answers if answered_by_all(group_answer, answer))

assert len(answers_answered_by_all(['kzardg', 'dkzgura', 'zdagrk', 'gdrak'], {'z', 'k', 'd', 'r', 'g', 'a', 'u'}).difference(['k', 'd', 'r', 'g', 'a'])) == 0

counters = list(len(answers_answered_by_all(ga, gau)) for (ga, gau) in zip(group_answers, group_answers_unique))

print(f"Sum of count of questions answered by all in group {sum(counters)}")