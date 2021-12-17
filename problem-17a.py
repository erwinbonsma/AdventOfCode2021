# Test
# xmin, xmax = 20, 30
# ymin, ymax = -10, -5

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

def max_height(vy):
    x = 0
    while vy > 0:
        x += vy
        vy -= 1
    return x

x_steps = set()
max_vx = xmax
vx = max_vx
while vx > 0:
    steps = steps_in_xrange(vx, xmin, xmax)
    print(vx, steps)

    if steps is not None:
        for step in range(steps[0], steps[1]):
            x_steps.add(step)
    vx -= 1

print(x_steps)

# y is a parabolic function. If vy is positive, y again crosses y = 0 with velocity -vy_initial.
# It's next y position is -(vy_initial + 1), which needs to be equal to or smaller than ymin for
# it not to overshoot the target area.
max_vy = abs(ymin) - 1
vy = max_vy
done = False
while not done:
    steps = steps_in_yrange(vy, ymin, ymax)
    print(steps)

    if steps is not None:
        # Check if there is an x-velocity so that the target area is reached within the step range
        for step in range(steps[0], steps[1]):
            if step in x_steps:
                print(vy, max_height(vy))
                done = True
    vy -= 1
