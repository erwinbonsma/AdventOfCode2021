
with open("input-03.txt") as fp:
    lines = [line for line in fp]

def filter_lines(filtered, find_common = True, pos = 0):
    print(pos, len(filtered))
    if len(filtered) == 1:
        return filtered[0]
    num_ones = sum(1 for _ in filter(lambda line: line[pos] == '1', filtered))
    if num_ones * 2 == len(filtered):
        wanted = '1' if find_common else '0'
    else:
        wanted = '1' if (num_ones * 2 > len(filtered)) == find_common else '0'
    return filter_lines(
        [line for line in filtered if line[pos] == wanted], find_common, pos + 1
    )

og_rating = filter_lines(lines, True)
cs_rating = filter_lines(lines, False)
print(int(og_rating, base = 2) * int(cs_rating, base = 2))