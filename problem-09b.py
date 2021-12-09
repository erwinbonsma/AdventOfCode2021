import itertools
import heapq
import math

map = []
with open("input-09.txt") as fp:
    map = [[int(ch) for ch in line.strip()] for line in fp]
w = len(map[0])
h = len(map)

def neighbours(x, y):
    if x > 0:
        yield (x - 1, y)
    if x < w - 1:
        yield (x + 1, y)
    if y > 0:
        yield (x, y - 1)
    if y < h - 1:
        yield (x, y + 1)

def is_low_point(x, y):
    for xn, yn in neighbours(x, y):
        if map[yn][xn] <= map[y][x]:
            return False
    return True

def basin_size(pos):
    pending = [pos]
    touched = set([pos])
    while len(pending) > 0:
        pos = pending.pop()
        for xn, yn in neighbours(*pos):
            if map[yn][xn] != 9 and not (xn, yn) in touched:
                touched.add((xn, yn))
                pending.append((xn, yn))
    return len(touched)

basin_sizes = []
for x, y in itertools.product(range(w), range(h)):
    if is_low_point(x, y):
        basin_sizes.append(basin_size((x, y)))

print(math.prod(heapq.nlargest(3, basin_sizes)))