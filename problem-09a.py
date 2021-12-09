import itertools

map = []
with open("input-09.txt") as fp:
    map = [[int(ch) for ch in line.strip()] for line in fp]
w = len(map[0])
h = len(map)

def is_low_point(x, y):
    if x > 0 and map[y][x - 1] <= map[y][x]:
        return False
    if x < w - 1 and map[y][x + 1] <= map[y][x]:
        return False
    if y > 0 and map[y - 1][x] <= map[y][x]:
        return False
    if y < h - 1 and map[y + 1][x] <= map[y][x]:
        return False
    return True

risk_level = 0
for x, y in itertools.product(range(w), range(h)):
    if is_low_point(x, y):
        risk_level += map[y][x] + 1

print(risk_level)