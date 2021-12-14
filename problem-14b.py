from collections import Counter, defaultdict

table = {}
with open("input-14.txt") as fp:
    polymer = next(fp).strip()
    assert(len(next(fp).strip()) == 0)

    for line in fp:
        line = line.strip()
        tokens = line.split(' ')
        assert(tokens[1] == '->')

        table[tokens[0]] = tokens[2]

polymer_pairs = Counter(ch1 + ch2 for ch1, ch2 in zip(polymer[0:], polymer[1:]))

def expand(polymer_pairs):
    map = defaultdict(int)
    for pair, num in polymer_pairs.items():
        ch = table[pair]
        map[pair[0] + ch] += num
        map[ch + pair[1]] += num
    return map

for _ in range(40):
    polymer_pairs = expand(polymer_pairs)

char_counts = defaultdict(int)
for pair, num in polymer_pairs.items():
    char_counts[pair[0]] += num
    char_counts[pair[1]] += num
char_counts[polymer[0]] += 1
char_counts[polymer[-1:]] += 1

print(max(char_counts.values()) // 2 - min(char_counts.values()) // 2)