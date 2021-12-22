import math
import re

status = []

def is_empty(cube):
    """
    >>> is_empty(((0, 3), (2, 5), (7, 9)))
    False

    >>> is_empty(((0, 0), (2, 2), (7, 7)))
    False

    >>> is_empty(((0, 0), (2, 1), (7, 7)))
    True
    """
    return any(lo > hi for lo, hi in cube)

def intersect(cube1, cube2):
    """
    >>> intersect(((-2, 2), (-3, 3), (-4, 4)), ((0, 5), (1, 4), (2, 3)))
    ((0, 2), (1, 3), (2, 3))

    >>> intersect(((-2, 2), (-3, 3), (-4, 4)), ((0, 5), (1, 4), (5, 8)))
    """
    intersection = tuple(
        (max(r1[0], r2[0]), min(r1[1], r2[1])) for r1, r2 in zip(cube1, cube2)
    )
    return None if is_empty(intersection) else intersection

def dump_cubes(cubes):
    for cube in cubes:
        print(cube)

def volume(cube):
    return math.prod(hi - lo + 1 for lo, hi in cube)

def subtract(cube, sub_cube):
    """
    >>> list(subtract(((0, 10), (0, 10), (0, 10)), ((0, 5), (0, 4), (7, 10))))
    [((6, 10), (0, 10), (0, 10)), ((0, 5), (5, 10), (0, 10)), ((0, 5), (0, 4), (0, 6))]

    >>> dump_cubes(subtract(((0, 10), (0, 10), (0, 10)), ((5, 6), (6, 7), (7, 8))))
    ((0, 4), (0, 10), (0, 10))
    ((7, 10), (0, 10), (0, 10))
    ((5, 6), (0, 5), (0, 10))
    ((5, 6), (8, 10), (0, 10))
    ((5, 6), (6, 7), (0, 6))
    ((5, 6), (6, 7), (9, 10))

    """
    for i in range(3):
        assert(cube[i][0] <= sub_cube[i][0])
        assert(cube[i][1] >= sub_cube[i][1])

        if cube[i][0] < sub_cube[i][0]:
            cube1 = tuple(
                bound if i != j else (cube[i][0], sub_cube[i][0] - 1) for j, bound in enumerate(cube)
            )
            cube2 = tuple(
                bound if i != j else (sub_cube[i][0], cube[i][1]) for j, bound in enumerate(cube)
            )
            return [cube1] + subtract(cube2, sub_cube)

        if cube[i][1] > sub_cube[i][1]:
            cube1 = tuple(
                bound if i != j else (sub_cube[i][1] + 1, cube[i][1]) for j, bound in enumerate(cube)
            )
            cube2 = tuple(
                bound if i != j else (cube[i][0], sub_cube[i][1]) for j, bound in enumerate(cube)
            )
            return [cube1] + subtract(cube2, sub_cube)
    return []

def update_status(status, new_cube, toggle_on = True):
    new_status = []
    for cube in status:
        overlap = intersect(cube, new_cube)
        if overlap is None:
            new_status.append(cube)
        else:
            new_status.extend(subtract(cube, overlap))

    if toggle_on:
        new_status.append(new_cube)
    
    return new_status

with open("input-22.txt") as fp:
    status = []
    for line in fp:
        cmd, cube = line.strip().split(' ')
        ranges = re.sub(r'[xyz]=', '', cube).split(',')
        bounds = tuple(
            tuple(int(v) for v in bounds.split('..')) for bounds in ranges
        )
        print(cmd, bounds)
        status = update_status(status, bounds, cmd == 'on')

    print(sum(volume(cube) for cube in status))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
