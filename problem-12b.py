paths = {}

with open("input-12.txt") as fp:
    for line in fp:
        line = line.strip()
        a, b = line.split('-')
        paths.setdefault(a, []).append(b)
        paths.setdefault(b, []).append(a)

def find_paths(node = 'start', visited = set(), total_paths = 0, repeat = None, path = []):
    #print(path, node, visited, repeat)
    is_small = node.islower()
    if is_small:
        if node == 'end':
            return total_paths + 1
        if node in visited:
            if repeat is None and node != 'start':
                repeat = node
            else:
                return total_paths
        else:
            visited.add(node)
    path.append(node)

    for next_node in paths[node]:
        total_paths = find_paths(next_node, visited, total_paths, repeat, path)

    path.pop()    
    if is_small:
        if repeat != node:
            visited.remove(node)
    return total_paths

print(find_paths())
