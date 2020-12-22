
lines = open("./day22/input.txt").read().splitlines()

init_p1 = list(int(e) for e in lines[1:26])
init_p2 = list(int(e) for e in lines[28:53])

player_1 = init_p1[::]
player_2 = init_p2[::]

print("==== Part 1 ====")

print(f"Player1: {player_1}")
print(f"Player2: {player_2}")

print("Starting the game")
while len(player_1) > 0 and len(player_2) > 0:
    v1 = player_1.pop(0)
    v2 = player_2.pop(0)
    if v1 > v2:
        player_1.append(v1)
        player_1.append(v2)
    elif v2 > v1:
        player_2.append(v2)
        player_2.append(v1)
    else:
        assert False
    # print(f"Next round {v1} vs {v2}")
    # print(f"Player1: {player_1}")
    # print(f"Player2: {player_2}")    

print("Game finished")

print(f"Player1: {player_1}")
print(f"Player2: {player_2}")

winner_score = player_1 if len(player_1) > 0 else player_2
asnwer_1 = sum((k+1)*v for k,v in enumerate(winner_score[::-1]))

print(f"Answer = {asnwer_1}")

assert asnwer_1 == 35299

print("==== Part 2 ====")

p1 = init_p1[::]
p2 = init_p2[::]

print(f"Player1: {p1}")
print(f"Player2: {p2}")

def serialize(a,b):
    return str(a) + str(b)

def start_sub_game(sp1, sp2, cache, index=0):
    # print(f"Starting the subgame {index} {sp1} {sp2}")
    history = set()
    while len(sp1) > 0 and len(sp2) > 0:
        if serialize(sp1,sp2) in history:
            # print(f"Loop detected {index} for {sp1} {sp2}")
            return 'p1'
        else:
            history.add(serialize(sp1,sp2))
        
        v1 = sp1.pop(0)
        v2 = sp2.pop(0)
        if len(sp1) >= v1 and len(sp2) >= v2:
            new_sp1 = sp1[:v1]
            new_sp2 = sp2[:v2]
            decks = serialize(new_sp1, new_sp2)
            if decks in cache:
                winner = cache[decks]
            else:
                winner = start_sub_game(new_sp1, new_sp2, cache)
                cache[decks] = winner
        else:
            winner = 'p1' if v1 > v2 else 'p2'
        
        if winner == 'p1':            
            sp1.append(v1)
            sp1.append(v2)
        else:
            sp2.append(v2)
            sp2.append(v1)

    # print(f"Finishing the subgame {index} {sp1} {sp2}")
    if len(sp1) == 0:
        return 'p2'
    else:
        return 'p1'

def start_game_v2(p1, p2):
    print("Starting the game")
    counter = 0
    cache = {}
    while len(p1) > 0 and len(p2) > 0:
        v1 = p1.pop(0)
        v2 = p2.pop(0)
        if len(p1) >= v1 and len(p2) >= v2:
            new_p1 = p1[:v1]
            new_p2 = p2[:v2]
            decks = serialize(new_p2, new_p2)
            if decks in cache:
                winner = cache[decks]
            else:
                winner = start_sub_game(new_p1, new_p2, cache)
                cache[decks] = winner
        else:
            winner = 'p1' if v1 > v2 else 'p2'       

        if winner == 'p1':
            p1.append(v1)
            p1.append(v2)
        else:
            p2.append(v2)
            p2.append(v1)        
        
        counter += 1        
        # print(f"Next round {counter}")
        # print(f"Player1: {p1}")
        # print(f"Player2: {p2}") 

start_game_v2(p1, p2)

print("Game finished")

print(f"Player1: {p1}")
print(f"Player2: {p2}")

winner_score_2 = p1 if len(p1) > 0 else p2
asnwer_2 = sum((k+1)*v for k,v in enumerate(winner_score_2[::-1]))

print(f"Answer = {asnwer_2}")

assert asnwer_2 == 33266

