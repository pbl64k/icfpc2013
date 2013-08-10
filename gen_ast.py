
import random
import copy

def gen_ast(sz, ops, vs):
    if 'tfold' in ops:
        ops0 = [x for x in ops if ops != 'tfold']
        while True:
            try:
                res = ['fold', 'x_0', '0', ['lambda', ['x_0', 'x_1'], gen_ast0(sz - 4, ops0, vs + 1, True)[1]]]
                return res
            except:
                continue
    else:
        while True:
            try:
                res = gen_ast0(sz, ops, vs, True)
                return res[1]
            except:
                continue

def gen_ast0(sz, ops, vs, last):
    if sz < 1:
        raise Exception()
    if last and sz == 1:
        my_ops = ['const', 'var']
    elif last and sz > 1:
        my_ops = copy.deepcopy(ops)
    else:   
        my_ops = copy.deepcopy(ops)
        my_ops += ['const', 'var']
    op = random.choice(my_ops)
    if op == 'const':
        return sz - 1, random.choice(['0', '1'])
    elif op == 'var':
        return sz - 1, 'x_' + str(random.randrange(vs))
    elif op in ['not', 'shl1', 'shr1', 'shr4', 'shr16']:
        nsz, ast = gen_ast0(sz - 1, ops, vs, last)
        if nsz < 0:
            raise Exception()
        return nsz, [op, ast]
    elif op in ['and', 'or', 'xor', 'plus']:
        nsz, ast1 = gen_ast0(sz - 2, ops, vs, False)
        nsz, ast2 = gen_ast0(nsz + 1, ops, vs, last)
        if nsz < 0:
            raise Exception()
        return nsz, [op, ast1, ast2]
    elif op == 'if0':
        nsz, ast1 = gen_ast0(sz - 3, ops, vs, False)
        nsz, ast2 = gen_ast0(nsz + 1, ops, vs, False)
        nsz, ast3 = gen_ast0(nsz + 1, ops, vs, last)
        if nsz < 0:
            raise Exception()
        return nsz, [op, ast1, ast2, ast3]
    elif op == 'fold':
        nsz, ast1 = gen_ast0(sz - 4, ops, vs, False)
        nsz, ast2 = gen_ast0(nsz + 1, ops, vs, False)
        nsz, ast3 = gen_ast0(nsz + 1, ops, vs + 2, last)
        if nsz < 0:
            raise Exception()
        return nsz, [op, ast1, ast2, ['lambda', ['x_' + str(vs), 'x_' + str(vs + 1)], ast3]]
    assert False

