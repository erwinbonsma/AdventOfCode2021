open_brackets  = "[{(<"
close_brackets = "]})>"

points = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

def parse(line):
    stack = []
    for ch in line:
        if ch in open_brackets:
            stack.append(ch)
        elif ch in close_brackets:
            assert(len(stack) > 0)
            open_bracket = stack.pop()
            if open_brackets.index(open_bracket) != close_brackets.index(ch):
                return 0
        else:
            print("Unexpected character")
            assert(False)
    score = 0
    for ch in reversed(stack):
        score = score * 5 + points[ch]
    return score

scores = []
with open("input-10.txt") as fp:
    scores = [score for score in (parse(line.strip()) for line in fp) if score > 0]

print(sorted(scores)[len(scores) // 2])