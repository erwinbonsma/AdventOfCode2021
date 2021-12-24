model_no_len = 14
# This program was used to verify the analysis of the MONAD program, as well as determine its
# output.
#
# The actual answers were found via manual exploration in Excel. In short, there are basically two
# types of program block in the MONAD program. These form pairs that should cancel each other out:
#
# 1) The first program block in the pair always adds a 26-base digit to the value in register Z.
#    Its input should be such that its sibling block can remove a digit.
# 
# 2) The second program block in the pair can remove a 26-base digit from the value in Z. Whether
#    or not this happens depends on the block's parameters, its input, and the input and parameter
#    of its sibling block.
# 
#    For the program input to be a MONAD number, this block must always remove a digit from the
#    value in Z.
#
# See eval_fast2 for the logic in both blocks. With this algorithm determined, the maximum and
# minimum MONAD number can be found by simple deduction, without search or trial and error.

num_regs = 4
block_size = 18

with open("input-24.txt") as fp:
    program = [tuple(line.strip().split(' ')) for line in fp]

def check_program():
    assert(len(program) == block_size * model_no_len)
    for i in range(block_size):
        if i == 4 or i == 5 or i == 15:
            print(i, list(program[j * block_size + i] for j in range(model_no_len)))
        else:
            for j in range(1, model_no_len):
                # print(i, j, program[i], program[j * block_size + i])
                assert(program[j * block_size + i] == program[i])

def extract_params():
    return [
        (int(program[i + 4][2]), int(program[i + 5][2]), int(program[i + 15][2])) 
        for i in (
            n * block_size for n in range(model_no_len)
        )
    ]

def reg_index(reg_name):
    return ord(reg_name) - ord('w')

def is_reg_name(reg_name):
    ch = reg_name[0]
    return ch >= 'w' and ch <= 'z'

def eval(number):
    assert(len(number) == model_no_len)

    input_index = 0
    regs = [0] * num_regs

    for i, instruction in enumerate(program):
        cmd = instruction[0]
        target_reg = reg_index(instruction[1])

        if cmd == "inp":
            regs[target_reg] = int(number[input_index])
            input_index += 1
            print("input", regs[target_reg])
            continue

        if is_reg_name(instruction[2]):
            value = regs[reg_index(instruction[2])]
        else:
            value = int(instruction[2])

        if cmd == "add":
            regs[target_reg] += value
        elif cmd == "mul":
            regs[target_reg] *= value
        elif cmd == "div":
            regs[target_reg] //= value
        elif cmd == "mod":
            regs[target_reg] = regs[target_reg] % value
        elif cmd == "eql":
            regs[target_reg] = 1 if regs[target_reg] == value else 0
        else:
            assert(False)

        if (i + 1) % block_size == 0 or True:
            print(regs)

    return regs[reg_index('z')]

block_params = extract_params()
print(block_params)

def eval_fast(number):
    w, x, y, z = [0] * num_regs
    for (ch, params) in zip(number, block_params):
        w = int(ch)
        x = z % 26
        z //= params[0]
        x += params[1]
        x = 0 if x == w else 1
        y = 25 * x + 1
        z *= y
        y = (w + params[2]) * x
        z += y
        print(z)
    
    return z

def eval_fast2(number):
    z = 0
    for (ch, params) in zip(number, block_params):
        w = int(ch)
        if params[0] == 1:
            z *= 26
            z += (w + params[2])
        else:
            x = z % 26
            z //= 26
            # This must hold for the value to be accepted by MONAD
            assert(x + params[1] == w)

        print(z)

check_program()

# The largest and smallest possible values
inputs = ["49917929934999", "11911316711816"]
for input in inputs:
    assert(eval(input) == 0)
    assert(eval_fast(input) == 0)
    c = eval_fast2(input)
