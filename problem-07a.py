with open("input-07.txt") as fp:
    positions = [int(pos) for pos in next(fp).split(',')]

print(min(
    sum(abs(pos - aim) for pos in positions)
    for aim in range(min(positions), max(positions) + 1)
))