from collections import Counter

table = {}
with open("input-14.txt") as fp:
    polymer = next(fp).strip()
    assert(len(next(fp).strip()) == 0)

    for line in fp:
        line = line.strip()
        tokens = line.split(' ')
        assert(tokens[1] == '->')

        table[tokens[0]] = tokens[2]

def expand(polymer):
    result = []
    for ch1, ch2 in zip(polymer[0:], polymer[1:]):
        result.append(ch1)
        result.append(table[ch1 + ch2])
    result.append(polymer[-1:])
    return ''.join(result)


for _ in range(10):
    polymer = expand(polymer)

char_counts = Counter(polymer)
print(max(char_counts.values()) - min(char_counts.values()))