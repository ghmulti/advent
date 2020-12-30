import math 

key1=18356117
key2=5909654

divider=20201227

def formula(loop_size, subject_number):
    result = 1
    for _ in range(loop_size):
        result = (result * subject_number) % divider
    return result


card_pk = formula(8, 7)
assert card_pk == 5764801
print(f"Card public key = {card_pk}")

door_pk = formula(11, 7)
assert door_pk == 17807724
print(f"Door public key = {door_pk}")

encryption_key = formula(8, door_pk)
assert encryption_key == 14897079
print(f"Encryption key {encryption_key}")

print(f"==== Part 1 ====")

n = 1
loop_size = 0
while n != key2:
    n = (n * 7) % divider
    loop_size += 1

print(f"Card public key loop size {loop_size}")
answer_1 = formula(loop_size, key1)
print(f"Encryption key {answer_1}")

assert answer_1 == 16902792
