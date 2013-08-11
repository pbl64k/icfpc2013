
from z3 import *

init('./Z3/z3-4.3.2.30df2837fbff-x86-ubuntu-12.04/bin/libz3.so')

#x = Int('x')
#y = Int('y')
#solve(x > 2, y < 10, x + 2*y == 7)
#
#x = BitVec('x', 8)
#solve(UGT(x, BitVecVal(0, 8)), x + x == BitVecVal(0, 8))

def solve_model(sz, operators, vals):
    s = Solver()

    zero = BitVecVal(0, 64)
    one = BitVecVal(1, 64)

    steps = sz - 2

    ops = []

    for step in range(steps):
        ops.append({})
        for op in operators:
            ops[step][op] = Int('ops_' + str(step) + '_' + op)
            s.add(Or(ops[step][op] == 0, ops[step][op] == 1))
        s.add(Sum(ops[step].values()) == 1)

    args = []

    for step in range(steps):
        args.append([{}])
        args[step][0]['zero'] = [zero, BitVec('args_' + str(step) + '_' + str(0) + '_' + 'zero', 64)]
        s.add(Or(args[step][0]['zero'][1] == 0, args[step][0]['zero'][1] == 1))
        args[step][0]['one'] = [one, BitVec('args_' + str(step) + '_' + str(0) + '_' + 'one', 64)]
        s.add(Or(args[step][0]['one'][1] == 0, args[step][0]['one'][1] == 1))
        args[step][0]['m_x'] = [None, BitVec('args_' + str(step) + '_' + str(0) + '_' + 'm_x', 64)]
        s.add(Or(args[step][0]['m_x'][1] == 0, args[step][0]['m_x'][1] == 1))

        for st in range(step):
            args[step][0]['svs_' + str(st)] = [None, BitVec('args_' + str(step) + '_' + str(0) + '_' + 'svs_' + str(st), 64)]
            s.add(Or(args[step][0]['svs_' + str(st)][1] == 0, args[step][0]['svs_' + str(st)][1] == 1))

        s.add(Sum(map(lambda x: x[1], args[step][0].values())) == 1)

    val_num = 0

    for x in vals:
        fx = vals[x]

        m_x = BitVecVal(x, 64)
        m_fx = BitVecVal(fx, 64)

        svs = []

        for step in range(steps):
            args[step][0]['m_x'][0] = m_x

            for st in range(step):
                args[step][0]['svs_' + str(st)][0] = svs[st]

            svs.append(BitVec('svs_' + str(val_num) + '_' + str(step), 64))

            s.add(Or(And(ops[step]['id'] == 1, gen_arg(args[step][0]) == svs[step]), \
                And(ops[step]['not'] == 1, ~gen_arg(args[step][0]) == svs[step])))

        s.add(m_fx == svs[steps - 1])

        val_num += 1

    print s.check()
    print s.model()

def gen_arg(args):
    expr = 0
    for k in args:
        val, var = args[k]
        expr += var * val
    return expr

solve_model(3, ['id', 'not'], {0: 0xffffffffffffffff, 2: 0xfffffffffffffffd})

# a sequence of steps, each step represents a creation of new value out of existing ones
# initial values are 0, 1 and x_0
# e.g., step 1 for ops not and shl1:
# v1 = y_1 * (not  (z_1_1 * 0 + z_1_2 * 1 + z_1_3 * x_0))
#    + y_2 * (shl1 (z_2_1 * 0 + z_2_2 * 1 + z_2_3 * x_0))
# where x, y - binary
# subject to:
# sum y = 1
# sum z = 1

# global:
#  must be a tree? all new values must be used exactly once - except for the result
#  enforce number of steps?
#  sum of ys for any given operator >= 1

