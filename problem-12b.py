paths = {}

with open("test-12.txt") as fp:
    for line in fp:
        line = line.strip()
        a, b = line.split('-')
        paths.setdefault(a, []).append(b)
        paths.setdefault(b, []).append(a)

def find_paths(node = 'start', visit_counts = {}, total_paths = 0, path = []):
    is_small = node.islower()
    if is_small:
        if node == 'end':
            print("==> ", path)
            return total_paths + 1
        max_count = 1 if node == 'start' else 2
        if visit_counts.setdefault(node, 0) == max_count:
            return total_paths
        visit_counts[node] += 1
    path.append(node)

    for next_node in paths[node]:
        total_paths = find_paths(next_node, visit_counts, total_paths, path)
    
    if is_small:
        visit_counts[node] -= 1
    path.pop()

    return total_paths

print(find_paths())
