import functools
import collections
import itertools

num_pos = 10
target_score = 21

outcomes = collections.Counter(
    3 + a + b + c for a, b, c in itertools.product(range(3), range(3), range(3))
)

def sum_tuples(tuple1, tuple2):
    return tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]

def multiply(num, tuple):
    return tuple[0] * num, tuple[1] * num

@functools.cache
def update_score(pos_a, pos_b, score_a, score_b):
    score_a += pos_a + 1
    if score_a >= target_score:
        return 1, 0
    wins_b, wins_a = play(pos_b, pos_a, score_b, score_a)
    return wins_a, wins_b

def play(pos_a, pos_b, score_a, score_b):
    return functools.reduce(
        sum_tuples, (
            multiply(occurences, update_score(
                (pos_a + die_sum) % num_pos, pos_b, score_a, score_b
            )) for die_sum, occurences in outcomes.items()
        )
    )

# print(play(3, 7, 0, 0)) # Test
print(play(6, 4, 0, 0)) # Problem