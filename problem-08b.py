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
digit_lookup = {
    s: n for n, s in enumerate(digits)
}

def unique(s, count = 1):
    char_counts = collections.Counter(s)
    unique_chars = [ch for ch in filter(lambda ch: char_counts[ch] == count, char_counts.keys())]
    assert(len(unique_chars) == 1)
    return unique_chars[0]

def find_mapping(signals):
    len_map = {}
    for signal in signals:
        len_map.setdefault(len(signal), []).append(signal)
    
    pos = [' ' for _ in range(7)]
    pos[0] = unique(len_map[2][0] + len_map[3][0])
    pos[5] = unique(len_map[2][0] + ''.join(len_map[6]), count = 4)
    pos[2] = unique(len_map[2][0] + pos[5])
    pos[4] = unique(len_map[4][0] + ''.join(len_map[6]), count = 2)
    pos[3] = unique(''.join(len_map[6]) + pos[2] + pos[4], count = 2)
    pos[1] = unique(len_map[4][0] + pos[2] + pos[3] + pos[5])
    pos[6] = unique(len_map[7][0] + ''.join(pos[i] for i in range(6)))

    return { ch: chr(n + ord('a')) for n, ch in enumerate(pos) }

def translate(s, mapping):
    remapped = [mapping[ch] for ch in s]
    return digit_lookup[''.join(sorted(remapped))]

summed_values = 0
with open("input-08.txt") as fp:
    for line in fp:
        line = line.strip()
        signals, display = line.split(' | ')
        mapping = find_mapping(signals.split(' '))
        digits = [translate(s, mapping) for s in display.split(' ')]

        value = int(''.join(str(d) for d in digits))
        summed_values += value

print(summed_values)
