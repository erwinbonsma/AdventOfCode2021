import re

def fold_x(dots, col):
    return set((x, y) if x < col else (2 * col - x, y) for x, y in dots)
def fold_y(dots, row):
    return set((x, y) if y < row else (x, 2 * row - y) for x, y in dots)

dots = set()
with open("input-13.txt") as fp:
    for line in fp:
        line = line.strip()
        if len(line) == 0:
            break
        x, y = line.split(',')
        dots.add((int(x), int(y)))

    for line in fp:
        line = line.strip()
        assert(line.startswith("fold along "))
        line = re.sub(r".* ", "", line)
        print(line)

        if line[0] == 'x':
            dots = fold_x(dots, int(line[2:]))
        elif line[0] == 'y':
            dots = fold_y(dots, int(line[2:]))
        else:
            assert(False)

w = max(x for x, _ in dots) + 1
h = max(y for _, y in dots) + 1
m = [[' '] * w for _ in range(h)]
for x, y in dots:
    m[y][x] = '*'

for row in m:
    print(''.join(row))