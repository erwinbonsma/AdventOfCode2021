num_players = 2
num_pos = 10
scores = [0] * num_players

# pos = [4, 8] # Test
pos = [7, 5] # Problem

def die_throw():
    num_throws = 0
    while True:
        # Returns die value, and number of throws, excluding this one
        yield num_throws % 100 + 1, num_throws
        num_throws = num_throws + 1

die = die_throw()
player = 0
while True:
    for _ in range(3):
        die_value, _ = next(die)
        pos[player] = (pos[player] + die_value - 1) % num_pos + 1
    scores[player] += pos[player]
    if scores[player] >= 1000:
        _, num_throws = next(die)
        print(scores[1 - player] * num_throws)
        break
    player = 1 - player
