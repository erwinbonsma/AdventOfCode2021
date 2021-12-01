with open("input-01a.txt") as fp:
    l = [int(line) for line in fp]
    print(sum(1 for _ in filter(lambda pair: pair[1] > pair[0], zip(l, l[1:]))))