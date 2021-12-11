from itertools import count, product

with open("input-11.txt") as fp:
    cave = [[int(ch) for ch in line.strip()] for line in fp]

w = len(cave[0])
h = len(cave)

def neighbours(x, y):
    for ix in range(max(0, x - 1), min(w - 1, x + 1) + 1):
        for iy in range(max(0, y - 1), min(h - 1, y + 1) + 1):
            if ix != x or iy != y:
                yield ix, iy

def update(cave):
    for x, y in product(range(w), range(h)):
        cave[y][x] += 1

    flashes = 0
    stop = False
    while not stop:
        stop = True
        for x, y in product(range(w), range(h)):
            if cave[y][x] == 10:
                flashes += 1
                stop = False
                cave[y][x] = 11
                for nx, ny in neighbours(x, y):
                    if cave[ny][nx] < 10:
                        cave[ny][nx] += 1

    for x, y in product(range(w), range(h)):
        if cave[y][x] == 11:
            cave[y][x] = 0

    return flashes

def dump(cave):
    for y in range(h):
        print(''.join(str(cave[y][x]) for x in range(w)))

for step in count(1):
    if update(cave) == w * h:
        print(step)
        dump(cave)
        break
