open_brackets  = "[{(<"
close_brackets = "]})>"

def parse(line):
    stack = []
    for n, ch in enumerate(line):
        if ch in open_brackets:
            stack.append(ch)
        elif ch in close_brackets:
            assert(len(stack) > 0)
            open_bracket = stack.pop()
            if open_brackets.index(open_bracket) != close_brackets.index(ch):
                print("Corrupt line:", '{0}_{1}_{2}'.format(line[0:n-1], ch, line[n+1:]))
                return ch
        else:
            print("Unexpected character")
            assert(False)
    return None

scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

score = 0
with open("input-10.txt") as fp:
    for line in fp:
        line = line.strip()
        corrupt_char = parse(line)
        if corrupt_char:
            score += scores[corrupt_char]

print(score)