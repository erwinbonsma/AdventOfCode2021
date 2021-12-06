from collections import Counter

with open("input-06.txt") as fp:
    states = [int(v) for v in next(fp).split(',')]

state_count_dict = Counter(states)
state_counts = [state_count_dict.get(key, 0) for key in range(9)]

num_days = 256
for _ in range(num_days):
    num_spawning = state_counts[0]
    state_counts = state_counts[1:] + [num_spawning]
    state_counts[6] += num_spawning
print(sum(state_counts))
