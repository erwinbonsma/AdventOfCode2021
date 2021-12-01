with open("input-01a.txt") as fp:
    l = [int(line) for line in fp]
    sw = [a + b + c for a, b, c in zip(l, l[1:], l[2:])]
    print(sum(1 for _ in filter(lambda pair: pair[1] > pair[0], zip(sw, sw[1:]))))