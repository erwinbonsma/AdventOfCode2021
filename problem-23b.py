import itertools

move_cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
num_rooms = 4
room_size = 4
num_corridor_pos = 7

rooms_target = ''.join(ch * room_size for ch in "ABCD")

def distance(room_index, corridor_pos):
    """Returns distance to room entrance"""
    if corridor_pos == 0:
        return room_index * 2 + 3
    if corridor_pos == 6:
        return 9 - room_index * 2
    if corridor_pos < room_index + 2:
        return (room_index + 2 - corridor_pos) * 2
    else:
        return (corridor_pos - room_index - 1) * 2

def target_room(ch):
    return ord(ch) - ord('A')

def target_pod(room_index):
    return chr(ord('A') + room_index)

class State:
    def __init__(self, rooms, corridor = ".......", cost = 0):
        self.rooms = rooms
        self.corridor = corridor
        self.cost = cost

    def dump(self):
        print("#" * 13, self.cost)
        print("#{0}{1}.{2}.{3}.{4}.{5}{6}#".format(*(ch for ch in self.corridor)))
        print("###{0}#{1}#{2}#{3}###".format(
            *(self.rooms[i*room_size] for i in range(num_rooms))
        ))
        for j in range(1, room_size):
            print("  #{0}#{1}#{2}#{3}#".format(
                *(self.rooms[i*room_size+j] for i in range(num_rooms))
            ))
        print("  #########")

    def is_solved(self):
        return self.rooms == rooms_target

    def room_contains_wrong_pods(self, room_index):
        ch_solve = chr(ord('A') + room_index)
        for j in range(room_size):
            ch = self.rooms[room_index * room_size + j]
            if ch != ch_solve and ch != '.':
                return True
        return False

    def is_path_free(self, room_index, corridor_pos):
        """Note: assumes the source and destination positions are free. It only checks the path
        between them"""
        if corridor_pos < room_index + 2:
            return all(self.corridor[i] == '.' for i in range(corridor_pos + 1, room_index + 2))
        else:
            return all(self.corridor[i] == '.' for i in range(room_index + 2, corridor_pos))

    def move_from_room(self, room_index, corridor_pos):
        room_pos = room_index * room_size
        while self.rooms[room_pos] == '.':
            room_pos += 1

        new_rooms = list(self.rooms)
        new_corridor = list(self.corridor)
        ch = new_rooms[room_pos]
        new_corridor[corridor_pos] = ch
        new_rooms[room_pos] = '.'

        cost_delta = move_cost[ch] * (distance(room_index, corridor_pos) + room_pos % room_size)
        return State(''.join(new_rooms), ''.join(new_corridor), self.cost + cost_delta)

    def move_to_room(self, room_index, corridor_pos):
        room_pos = (room_index + 1) * room_size - 1
        while self.rooms[room_pos] != '.':
            room_pos -= 1

        new_rooms = list(self.rooms)
        new_corridor = list(self.corridor)
        ch = new_corridor[corridor_pos]
        new_rooms[room_pos] = ch
        new_corridor[corridor_pos] = '.'

        cost_delta = move_cost[ch] * (distance(room_index, corridor_pos) + room_pos % room_size)
        return State(''.join(new_rooms), ''.join(new_corridor), self.cost + cost_delta)

    def next_states(self):
        states = []

        # Try and move from every room
        for room_index in range(num_rooms):
            if self.room_contains_wrong_pods(room_index):
                for corridor_pos in range(num_corridor_pos):
                    if self.corridor[corridor_pos] == '.' \
                    and self.is_path_free(room_index, corridor_pos):
                        states.append(self.move_from_room(room_index, corridor_pos))

        # Try and move into rooms
        for corridor_pos in range(num_corridor_pos):
            if self.corridor[corridor_pos] != '.':
                room_index = target_room(self.corridor[corridor_pos])
                if not self.room_contains_wrong_pods(room_index) \
                and self.is_path_free(room_index, corridor_pos):
                    states.append(self.move_to_room(room_index, corridor_pos))

        return states

    def is_valid(self):
        if sum(1 for ch in itertools.chain(self.rooms, self.corridor) if ch != '.') != room_size * num_rooms:
            return False
        for i in range(num_rooms):
            for j in range(room_size - 1):
                if self.rooms[i * room_size + j] != '.' \
                and self.rooms[i * room_size + j + 1] == '.':
                    return False
        return True

    def __key(self):
        return (self.rooms, self.corridor, self.cost)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, State):
            return self.__key() == other.__key()
        return False

def solve_breadth_first(state):
    """Try solve using breadth-first search"""
    pending_states = {0: [state]}
    while len(pending_states):
        costs = list(pending_states.keys())
        costs.sort()
        next_cost = costs[0]
        print("Cost", next_cost)
        for state in pending_states[next_cost]:
            if state.is_solved():
                print("Solved with cost", state.cost)
                return
            for next_state in state.next_states():
                pending_states.setdefault(next_state.cost, set()).add(next_state)
        del pending_states[next_cost]

best_level = 0
max_level = num_rooms * room_size * 2

def solve(state, best_sofar = 999999, level = 0):
    assert(level <= max_level)
    global best_level
    if level > best_level:
        best_level = level
        print(best_level)
        state.dump()

    if state.cost > best_sofar:
        return best_sofar

    for next_state in state.next_states():
        if next_state.is_solved():
            if next_state.cost < best_sofar:
                best_sofar = next_state.cost
                print("Found solution", best_sofar)
        else:
            best_sofar = min(best_sofar, solve(next_state, best_sofar, level + 1))

    return best_sofar

# Test
#state = State("BDDACCBDBBACDACA")
#state = State("BACDBCDA")

# Input
state = State("DDDDACBCCBABAACB")

#solve(state)
solve_breadth_first(state)
