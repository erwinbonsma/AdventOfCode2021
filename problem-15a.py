risk = []
with open("input-15.txt") as fp:
    for line in fp:
        risk.append([int(ch) for ch in line.strip()])

w = len(risk[0])
h = len(risk)

def neighbours(pos):
    x, y = pos
    if x > 0:
        yield (x - 1, y)
    if x < w - 1:
        yield (x + 1, y)
    if y > 0:
        yield (x, y - 1)
    if y < h - 1:
        yield (x, y + 1)

inf = 9999
def find_min_path(x0 = 0, y0 = 0):
    dist = {
        (x, y): inf for x in range(w) for y in range(h)
    }
    current = (x0, y0)
    dist[current] = 0
    visited = set()
    candidates = set()
    while True:
        for nb_pos in neighbours(current):
            if nb_pos not in visited:
                dist[nb_pos] = min(dist[nb_pos], dist[current] + risk[nb_pos[1]][nb_pos[0]])
                candidates.add(nb_pos)
        visited.add(current)

        if len(candidates) == 0:
            break

        min_dist = inf
        for n in candidates:
            if dist[n] < min_dist:
                min_dist = dist[n]
                current = n
        assert(min_dist < inf)
        candidates.remove(current)
    return dist[(w - 1, h - 1)]

print(find_min_path())
