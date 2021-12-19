min_matches = 12

class Orientation:
    def __init__(self, spec):
        self.spec = spec

    def transform(self, pos):
        return (
            pos[self.spec[0]] * self.spec[3],
            pos[self.spec[1]] * self.spec[4],
            pos[self.spec[2]] * self.spec[5]
        )

def x_rotate(spec):
    return (spec[0], spec[2], spec[1], spec[3], -spec[5], spec[4])

def y_rotate(spec):
    return (spec[2], spec[1], spec[0], spec[5], spec[4], -spec[3])

def z_rotate(spec):
    return (spec[1], spec[0], spec[2], -spec[4], spec[3], spec[5])

def create_orientations():
    orientations = []
    spec = (0, 1, 2, 1, 1, 1)
    for _ in range(4):
        orientations.append(Orientation(spec))
        orientations.append(Orientation(x_rotate(spec)))
        orientations.append(Orientation(x_rotate(x_rotate(spec))))
        orientations.append(Orientation(x_rotate(x_rotate(x_rotate(spec)))))
        orientations.append(Orientation(y_rotate(spec)))
        orientations.append(Orientation(y_rotate(y_rotate(y_rotate(spec)))))
        spec = z_rotate(spec)
    assert(len(orientations) == 24)
    return orientations

orientations = create_orientations()

class Scanner:
    def __init__(self, id):
        self.id = id
        self.beacons = []
        self.relation = None

    def add_beacon(self, pos):
        self.beacons.append(pos)

    def create_signature(self):
        self.distances = {}
        for i in range(len(self.beacons)):
            for j in range(i + 1, len(self.beacons)):
                dist = sum(abs(a - b) for a, b in zip(self.beacons[i], self.beacons[j]))
                self.distances.setdefault(dist, []).append((i, j))

    def process(self):
        self.beacons_rot = {}
        for rot in orientations:
            self.beacons_rot[rot] = [rot.transform(pos) for pos in self.beacons]

    def has_beacon(self, pos):
        return any(beacon == pos for beacon in self.beacons)

    def position(self):
        pos = (0, 0, 0)
        scanner = self
        while scanner.relation is not None:
            other, rel_pos, rot = scanner.relation
            pos = tuple(a + b for a, b in zip(rot.transform(pos), rel_pos))
            scanner = other
        return pos

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    def dump(self):
        print("id =", self.id)
        for beacon in self.beacons:
            print(beacon)
        print(self.distances)

def read_input(filename):
    scanners = []
    scanner = None
    with open(filename) as fp:
        for line in fp:
            line = line.strip()

            if scanner is None:
                assert(line.startswith("---"))
                scanner = Scanner(line[4:-4])
                scanners.append(scanner)
                continue

            if len(line) == 0:
                scanner = None
                continue

            scanner.add_beacon(tuple(int(v) for v in line.split(',')))
    return scanners

def try_align(s1, s2, b1, b2, s2_orientation):
    num_matches = 0
    s2_beacons_rot = s2.beacons_rot[s2_orientation]
    s2_pos = tuple(
        a - b for a, b in zip(s1.beacons[b1], s2_beacons_rot[b2])
    )
    for beacon in s2_beacons_rot:
        # The position of the S2 beacon expressed in S1 coordinates
        b2_pos = tuple(
            a + b for a, b in zip(beacon, s2_pos)
        )
        if max(abs(v) for v in b2_pos) <= 1000:
            if s1.has_beacon(b2_pos):
                num_matches += 1
            else:
                return None

    return s2_pos if num_matches >= min_matches else None

def find_match(scanner1, scanner2):
    for i in range(len(scanner1.beacons) - min_matches + 1):
        for j in range(len(scanner2.beacons)):
            for o2 in orientations:
                scanner2_pos = try_align(scanner1, scanner2, i, j, o2)
                if scanner2_pos is not None:
                    return scanner2_pos, o2
    return None, None



def extend_map(beacon_map, scanner):
    beacon_positions = [beacon for beacon in scanner.beacons]

    while scanner.relation is not None:
        other, scanner_pos, scanner_rot = scanner.relation
        beacon_positions = [
            tuple(a + b for a, b in zip(
                scanner_pos,
                scanner_rot.transform(pos)
            )) for pos in beacon_positions
        ]
        scanner = other

    beacon_map.update(beacon_positions)

def connect_scanners():
    pending = [scanners[0]]
    unconnected = scanners[1:]
    all_beacons = set(b for b in scanners[0].beacons)

    while len(pending) > 0:
        s1 = pending.pop()

        for s2 in unconnected[:]:
            s2_pos, s2_rot = find_match(s1, s2)
            if s2_pos is not None:
                print('Connected {0} and {1} at {2}'.format(s1.id, s2.id, s2_pos))

                pending.append(s2)                
                unconnected.remove(s2)

                s2.relation = (s1, s2_pos, s2_rot)
                extend_map(all_beacons, s2)

    assert(len(unconnected) == 0)

    print(len(all_beacons))

scanners = read_input("input-19.txt")

for scanner in scanners:
    scanner.process()
connect_scanners()

for scanner in scanners:
    print(scanner.id, scanner.position())

print("Max distance =", max(
    sum(abs(a - b) for a, b in zip(
        s1.position(),
        s2.position()
    ))
    for s1 in scanners
    for s2 in scanners
))