import itertools

with open("input-25.txt") as fp:
    state = [list(line.strip()) for line in fp]

w = len(state[0])
h = len(state)

dirs = {
    '>': (1, 0),
    'v': (0, 1)
}

def char_at(state, x, y):
    return state[(y + h) % h][(x + w) % w]

def can_move(state, x, y, move_char):
    dx, dy = dirs[move_char]

    if char_at(state, x, y) != move_char:
        return False
    if char_at(state, x + dx, y + dy) != '.':
        return False

    return True

def update(state, move_char):
    new_state = [[None] * w for _ in range(h)]
    dx, dy = dirs[move_char]
    num_moved = 0

    for x in range(w):
        for y in range(h):
            moving = can_move(state, x, y, move_char)
            new_state[y][x] = (
                '.' if moving else (
                    move_char if can_move(state, x - dx, y - dy, move_char) else char_at(state, x, y)
                )
            )
            if moving:
                num_moved += 1
    
    return new_state, num_moved

def update_state(state):
    state, num_moved1 = update(state, '>')
    state, num_moved2 = update(state, 'v')
    return state, num_moved1 + num_moved2

def dump(state):
    for y in range(h):
        print(''.join(state[y]))

for step in itertools.count():
    print(step + 1)

    state, num_moved = update_state(state)

    if num_moved == 0:
        break