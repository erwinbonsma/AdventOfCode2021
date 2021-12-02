x = 0
depth = 0 
aim = 0
with open("input-02.txt") as fp:
    for line in fp:
        args = line.split(' ')
        cmd = args[0]
        amount = int(args[1])
        print(cmd, amount)
        if cmd == "forward":
            x += amount
            depth += amount * aim
        elif cmd == "down":
            aim += amount
        elif cmd == "up":
            aim -= amount
        else:
            assert(False)
print(x * depth)