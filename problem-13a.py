import re

dots = set()

def fold_x(dots, col):
    return set((x, y) if x < col else (2 * col - x, y) for x, y in dots)
def fold_y(dots, row):
    return set((x, y) if y < row else (x, 2 * row - y) for x, y in dots)

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
            assert(false)
        print("# = ", len(dots))
