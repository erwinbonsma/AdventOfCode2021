border = 55

class Grid:
    def __init__(self, width):
        self.width = width
        self.height = 0
        self.grid = []

    def add_row(self, row):
        assert(len(row) == self.width)
        self.grid.append(row)
        self.height += 1

    def index(self, x, y):
        if x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1:
            return 0 if self.grid[0][0] == 0 else 511

        val = 0
        for i in range(9):
            val = val << 1
            dx = i % 3 - 1
            dy = i // 3 - 1
            val += self.grid[y + dy][x + dx]

        return val

    def show(self):
        for row in self.grid:
            print(''.join('#' if v == 1 else '.' for v in row))

    def step(self):
        new_grid = []
        for y in range(self.height):
            new_grid.append([0] * self.width)
            for x in range(self.width):
                new_grid[y][x] = mapping[self.index(x, y)]
        
        self.grid = new_grid

    def num_lit(self):
        return sum(len([v for v in row if v == 1]) for row in self.grid)

with open("input-20.txt") as fp:
    mapping = [1 if ch == '#' else 0 for ch in next(fp).strip()]

    next(fp)

    grid = None
    for line in fp:
        line = line.strip()
        if grid is None:
            grid = Grid(len(line) + 2 * border)
            for _ in range(border):
                grid.add_row([0] * grid.width)
        row = [0] * grid.width
        for i, ch in enumerate(line):
            if ch == '#':
                row[i + border] = 1
        grid.add_row(row)

    for _ in range(border):
        grid.add_row([0] * grid.width)

grid.show()
for _ in range(50):
    grid.step()
    #grid.show()
    print(grid.num_lit())
