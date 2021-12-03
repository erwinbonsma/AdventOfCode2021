num = 0
counts = None

with open("input-03.txt") as fp:
    for line in fp:
        if counts is None:
            counts = [0 for _ in range(len(line) - 1)]
        for i,bit in enumerate(line):
            if bit == '1':
                counts[i] += 1
        num += 1

for n, _ in filter(lambda tuple: tuple[1] * 2 == num, enumerate(counts)):
    print("Warning: tie at position", n)

gamma = ''.join(['1' if count * 2 > num else '0' for count in counts])
gamma_val = int(gamma, base = 2)
epsilon_val = pow(2, len(counts)) - gamma_val - 1
print(gamma_val, epsilon_val, gamma_val * epsilon_val)