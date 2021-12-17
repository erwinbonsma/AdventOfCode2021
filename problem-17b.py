from collections import defaultdict

# Test
#xmin, xmax = 20, 30
#ymin, ymax = -10, -5

# Input
xmin, xmax = 88, 125
ymin, ymax = -157, -103

max_steps = 1000

def steps_in_xrange(vx, xmin, xmax):
    x = 0
    steps = 0
    min_step = None
    while x <= xmax:
        if x >= xmin and min_step is None:
            min_step = steps
        x += vx
        if vx > 0:
            vx -= 1
        else:
            if min_step is not None:
                steps = max_steps
            break
        steps += 1
    if min_step is None:
        return None
    else:
        return [min_step, steps]

def steps_in_yrange(vy, ymin, ymax):
    y = 0
    steps = 0
    min_step = None
    while y >= ymin:
        if y <= ymax and min_step is None:
            min_step = steps
        y += vy
        vy = vy - 1
        steps += 1
    if min_step is None:
        return None
    else:
        # Returns range of steps. Upper bound is exclusive!
        return [min_step, steps]

step_to_vx_set = {}
max_vx = xmax
vx = max_vx
while vx > 0:
    steps = steps_in_xrange(vx, xmin, xmax)

    if steps is not None:
        for step in range(steps[0], steps[1]):
            step_to_vx_set.setdefault(step, set()).add(vx)
    vx -= 1

# y is a parabolic function. If vy is positive, y again crosses y = 0 with velocity -vy_initial.
# It's next y position is -(vy_initial + 1), which needs to be equal to or smaller than ymin for
# it not to overshoot the target area.
max_vy = abs(ymin) - 1
min_vy = ymin
vy = max_vy

count = 0
while vy >= min_vy:
    steps = steps_in_yrange(vy, ymin, ymax)

    if steps is not None:
        vx_set = set()
        for step in range(steps[0], steps[1]):
            vx_set.update(step_to_vx_set.setdefault(step, set()))
        count += len(vx_set)

    vy -= 1

print(count)