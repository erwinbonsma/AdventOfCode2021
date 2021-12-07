with open("input-07.txt") as fp:
    positions = [int(pos) for pos in next(fp).split(',')]

def fuel_consumption(d):
    return d * (d + 1) // 2

print(min(
    sum(fuel_consumption(abs(pos - aim)) for pos in positions)
    for aim in range(min(positions), max(positions) + 1)
))