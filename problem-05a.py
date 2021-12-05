from itertools import chain

size = 1000
counts = [
    [0 for _ in range(size)] for _ in range(size)
]

def mark_vertical_line(x, y1, y2, counts):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        counts[y][x] += 1

def mark_horizontal_line(y, x1, x2, counts):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        counts[y][x] += 1

with open("input-05.txt") as fp:
    for line in fp:
        fields = line.split(' ')
        x1, y1 = [int(v) for v in fields[0].split(',')]
        assert(fields[1] == '->')
        x2, y2 = [int(v) for v in fields[2].split(',')]

        if x1 == x2:
            mark_vertical_line(x1, y1, y2, counts)
        elif y1 == y2:
            mark_horizontal_line(y1, x1, x2, counts)

print(sum(1 for _ in filter(lambda v: v > 1, chain(*counts))))