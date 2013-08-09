
from bv_meta import *

import copy

mask_8 = 0b11111111
mask_64 = 0b1111111111111111111111111111111111111111111111111111111111111111

def evl(p, x):
    assert valid(p)
    return eval0(p[2], {p[1][0]: x})

def eval0(x, v):
    if valid_const(x):
        return int(x) & mask_64
    if valid_ident(x):
        assert x in v
        return v[x] & mask_64
    if valid_if(x):
        c = eval0(x[1], v)
        if c == 0:
            return eval0(x[2], v)
        else:
            return eval0(x[3], v)
    if valid_fold(x):
        return eval_fold(x, v)
    if valid_op1(x):
        return eval_op1(x[0], eval0(x[1], v))
    if valid_op2(x):
        return eval_op2(x[0], eval0(x[1], v), eval0(x[2], v))
    assert False

def eval_fold(x, v):
    c = eval0(x[1], v)
    byte = map(lambda z: (c >> (z * 8)) & mask_8, range(8))
    def l(a, b):
        v0 = copy.deepcopy(v)
        v0[x[3][1][0]] = b
        v0[x[3][1][1]] = a
        return eval0(x[3][2], v0)
    return reduce(l, byte, eval0(x[2], v))

def eval_op1(op, x):
    if op == 'not':
        return ~x & mask_64
    if op == 'shl1':
        return (x << 1) & mask_64
    if op == 'shr1':
        return (x >> 1) & mask_64
    if op == 'shr4':
        return (x >> 4) & mask_64
    if op == 'shr16':
        return (x >> 4) & mask_64
    assert False
    
def eval_op2(op, x, y):
    if op == 'and':
        return (x & y) & mask_64
    if op == 'or':
        return (x | y) & mask_64
    if op == 'xor':
        return (x ^ y) & mask_64
    if op == 'plus':
        return (x + y) & mask_64
    assert False

if __name__ == '__main__':
    assert bin(eval0(parse('(not 1)'), {})) == '0b1111111111111111111111111111111111111111111111111111111111111110'
    assert evl(parse('(lambda (x) (fold x 0 (lambda (y z) (or y z))))'), 0x1122334455667788) == 255
    assert evl(parse('(lambda (x) (fold x 1 (lambda (y z) (and y z))))'), 0x8141211109050301) == 1

