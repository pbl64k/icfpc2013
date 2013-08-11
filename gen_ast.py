
from bv_meta import *

import random
import copy

def itr_ast(sz, ops):
    for x in itr_ast0(sz - 1, ops, 1):
        yield ['lambda', ['x_0'], x]

def itr_ast0(sz, ops, vs):
    if 'tfold' in ops:
        ops0 = [x for x in ops if ops != 'tfold']
        for x in itr_ast1(sz - 4, ops0, vs + 1, True):
            yield ['fold', 'x_0', '0', ['lambda', ['x_0', 'x_1'], x[1]]]
    else:
        for x in itr_ast1(sz, ops, vs, True):
            yield x[1]

def itr_ast1(sz, ops, vs, last):
    if sz > 0:
        if last and sz == 1:
            my_ops = ['const', 'var']
        elif last and sz > 1:
            my_ops = copy.deepcopy(ops)
        else:   
            my_ops = copy.deepcopy(ops)
            my_ops += ['const', 'var']
        for op in my_ops:
            if op == 'const':
                for c in ['0', '1']:
                    yield sz - 1, c
            elif op == 'var':
                for v in range(vs):
                    yield sz - 1, 'x_' + str(v)
            elif op in ['not', 'shl1', 'shr1', 'shr4', 'shr16']:
                for nsz, ast in itr_ast1(sz - 1, ops, vs, last):
                    if nsz >= 0:
                        yield nsz, [op, ast]
            elif op in ['and', 'or', 'xor', 'plus']:
                for nsz1, ast1 in itr_ast1(sz - 2, ops, vs, False):
                    for nsz2, ast2 in itr_ast1(nsz1 + 1, ops, vs, last):
                        if nsz2 >= 0:
                            yield nsz1, [op, ast1, ast2]
            elif op == 'if0':
                for nsz1, ast1 in itr_ast1(sz - 3, ops, vs, False):
                    for nsz2, ast2 in itr_ast1(nsz1 + 1, ops, vs, False):
                        for nsz3, ast3 in itr_ast1(nsz2 + 1, ops, vs, last):
                            if nsz3 >= 0:
                                yield nsz3, [op, ast1, ast2, ast3]
            elif op == 'fold':
                for nsz1, ast1 in itr_ast1(sz - 4, ops, vs, False):
                    for nsz2, ast2 in itr_ast1(nsz1 + 1, ops, vs, False):
                        for nsz3, ast3 in itr_ast1(nsz2 + 1, ops, vs + 2, last):
                            if nsz3 >= 0:
                                yield nsz3, [op, ast1, ast2, ['lambda', ['x_' + str(vs), 'x_' + str(vs + 1)], ast3]]

def gen_ast(sz, ops, vs, flip):
    if 'tfold' in ops:
        ops0 = [x for x in ops if ops != 'tfold']
        while True:
            try:
                res = ['fold', 'x_0', '0', ['lambda', ['x_0', 'x_1'], gen_ast0(sz - 4, ops0, vs + 1, flip)[1]]]
                return res
            except:
                continue
    elif 'bonus' in ops:
        ops0 = [x for x in ops if ops != 'bonus']
        while True:
            try:
                nsz1, ast1 = gen_ast0(sz - 3, ops0, vs, False)
                nsz2, ast2 = gen_ast0(nsz1 + 1, ops0, vs, False)
                nsz3, ast3 = gen_ast0(nsz2 + 1, ops0, vs, flip)
                if nsz3 < 0:
                    continue
                res = ['if0', ast1, ast2, ast3]
                return res
            except:
                continue
    else:
        while True:
            try:
                res = gen_ast0(sz, ops, vs, flip)
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

if __name__ == '__main__':
    for p in itr_ast(6, ['shr1', 'not', 'plus']):
        print gen(p)

