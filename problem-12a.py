paths = {}

with open("input-12.txt") as fp:
    for line in fp:
        line = line.strip()
        a, b = line.split('-')
        paths.setdefault(a, []).append(b)
        paths.setdefault(b, []).append(a)

def find_paths(node = 'start', visited = set(), count = 0):
    is_small = node.islower()
    if is_small:
        if node in visited:
            return count
        elif node == 'end':
            return count + 1
        else:
            visited.add(node)

    for next_node in paths[node]:
        count = find_paths(next_node, visited, count)
    
    if is_small:
        visited.remove(node)
    return count

print(find_paths())
