with open("input-06.txt") as fp:
    state = [int(v) for v in next(fp).split(',')]

num_days = 80
for _ in range(num_days):
    state = [v - 1 for v in state]
    state.extend(8 for v in filter(lambda v: v <= 0 and v % 7 == 6, state))
print(len(state))
