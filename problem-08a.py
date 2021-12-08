import collections

digits = [
    'abcefg',  # 0
    'cf',      # 1
    'acdeg',   # 2
    'acdfg',   # 3
    "bcdf",    # 4
    "abdfg",   # 5
    "abdefg",  # 6
    "acf",     # 7
    "abcdefg", # 8
    "abcdfg",  # 9
]
len_counts = collections.Counter(len(d) for d in digits)
unique_lens = set(filter(lambda x: len_counts.get(x, 0) == 1, range(10)))

print(unique_lens)

hits = 0
with open("input-08.txt") as fp:
    for line in fp:
        line = line.strip()
        signals, display = line.split(' | ')
        print(display)
        hits += sum(
            1 if len(digit) in unique_lens else 0
            for digit in display.split(' ')
        )

print(hits)