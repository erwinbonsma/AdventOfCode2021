
def try_explode(pair, depth = 0):
    """
    >>> try_explode([[[[[9,8],1],2],3],4])
    True
    >>> try_explode([[[[0,9],2],3],4])
    False
    >>> try_explode([7,[6,[5,[4,[3,2]]]]])
    True
    >>> try_explode([7,[6,[5,[7,0]]]])
    False
    """
    if depth == 4:
        return True
    for n in range(2):
        if type(pair[n]) == list and try_explode(pair[n], depth + 1):
            return True
    return False

def add_right(x, value):
    if value == 0:
        return x
    if type(x) == list:
        return [x[0], add_right(x[1], value)]
    else:
        return x + value

def add_left(x, value):
    if value == 0:
        return x
    if type(x) == list:
        return [add_left(x[0], value), x[1]]
    else:
        return x + value

def explode(pair, depth = 0):
    """
    >>> explode([[[[[9,8],1],2],3],4])
    ([[[[0, 9], 2], 3], 4], 9, 0, True)

    >>> explode([[[[0,9],2],3],4])
    ([[[[0, 9], 2], 3], 4], 0, 0, False)
    
    >>> explode([7,[6,[5,[4,[3,2]]]]])
    ([7, [6, [5, [7, 0]]]], 0, 2, True)

    >>> explode([7,[6,[5,[7,0]]]])
    ([7, [6, [5, [7, 0]]]], 0, 0, False)
    
    >>> explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
    ([[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]], 0, 0, True)

    >>> explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
    ([[3, [2, [8, 0]]], [9, [5, [7, 0]]]], 0, 2, True)
    """
    if depth == 4:
        return 0, pair[0], pair[1], True

    for n in range(2):
        if type(pair[n]) == list:
            new_value, left, right, exploded = explode(pair[n], depth + 1)
            #print(new_value, left, right, exploded)
            if exploded:
                if n == 0:
                    return [new_value, add_left(pair[1], right)], left, 0, True
                elif n == 1:
                    return [add_right(pair[0], left), new_value], 0, right, True

    return pair, 0, 0, False

def split(x):
    """
    >>> split([[[[0,7],4],[15,[0,13]]],[1,1]])
    ([[[[0, 7], 4], [[7, 8], [0, 13]]], [1, 1]], True)

    >>> split([[[[0,7],4],[[7,8],[0,13]]],[1,1]])
    ([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]], True)

    >>> split([[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]])
    ([[[[0, 7], 4], [[7, 8], [0, [6, 7]]]], [1, 1]], False)
    """
    if type(x) == int:
        if x >= 10:
            return [x // 2, (x + 1) // 2], True
        else:
            return x, False

    for n in range(2):
        new_value, did_split = split(x[n])
        if did_split:
            if n == 0:
                return [new_value, x[1]], True
            else:
                return [x[0], new_value], True

    return x, False

def reduce(pair):
    """
    >>> reduce([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]])
    [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    """
    while True:
        pair, _, _, exploded = explode(pair)
        if exploded:
            continue

        pair, did_split = split(pair)
        if did_split:
            continue

        return pair

def add(pair1, pair2):
    """
    >>> add([[[[4,3],4],4],[7,[[8,4],9]]], [1,1])
    [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
    """
    return reduce([pair1, pair2])

def magnitude(x):
    """
    >>> magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
    1384

    >>> magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])
    3488
    """

    if type(x) == int:
        return x
    
    return 3 * magnitude(x[0]) + 2 * magnitude(x[1])

def find_comma(s):
    pos = 0
    level = 0
    while level > 1 or s[pos] != ',':
        if s[pos] == '[':
            level += 1
        elif s[pos] == ']':
            level -= 1
        pos += 1
    return pos

def parse_string(s):
    """
    >>> parse_string("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]")
    [[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]]
    """
    if s[0] == '[':
        assert(s[-1:] == ']')
        comma_pos = find_comma(s)
        return [
            parse_string(s[1 : comma_pos]),
            parse_string(s[comma_pos + 1 : -1])
        ]
    return int(s)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    with open("input-18.txt") as fp:
        pairs = [parse_string(line.strip()) for line in fp]

    print(
        max(
            magnitude(add(pairs[i], pairs[j]))
            for i in range(len(pairs))
            for j in range(len(pairs))
            if i != j
        )
    )