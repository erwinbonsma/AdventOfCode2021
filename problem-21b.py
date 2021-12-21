import functools
import collections
import itertools

num_pos = 10
target_score = 21

outcomes = collections.Counter(
    3 + a + b + c for a, b, c in itertools.product(range(3), range(3), range(3))
)

def update_score(pos_a, pos_b, score_a, score_b, count):
    score_a += pos_a + 1
    if score_a >= target_score:
        return count, 0
    wins_b, wins_a = play(pos_b, pos_a, score_b, score_a, count)
    return wins_a, wins_b

def play(pos_a, pos_b, score_a, score_b, count = 1):
    return functools.reduce(
        lambda x, y: (x[0] + y[0], x[1] + y[1]), (
            update_score(
                (pos_a + die_sum) % num_pos, pos_b, score_a, score_b, count * occurences
            ) for die_sum, occurences in outcomes.items()
        )
    )

# print(play(3, 7, 0, 0)) # Test
print(play(6, 4, 0, 0)) # Problem