
from bv_parser import parse
from bv_meta import *
from bv import evl

import copy
import random

def process(logger, cl, resp, force = False):
    for x in resp:
        solved = 'solved' in x and x['solved']
        if not solved:
            logger('size: %d ops: %s id: %s %s %s\n' % \
                (x['size'], str(x['operators']), x['id'], \
                ('SOLVED!' if solved else 'unsolved.'), \
                (('time: ' + str(x['timeLeft'])) if 'timeLeft' in x and x['timeLeft'] > 0 else '')))
        if not force and (solved or ('timeLeft' in x and x['timeLeft'] == 0)):
            continue
        if x['size'] > 10:
            return False
        if x['size'] == 3 and len(x['operators']) == 1:
            logger('\nSolving...\n')
            code = solve_3(x['id'], x['size'], x['operators'])
            logger(code + '\n')
            p = parse(code)
            logger(str(p) + '\n')
            logger(str(sz(p)) + '\n')
            logger(str(ops(p)) + '\n\n')
            cl.guess(x['id'], code)
            return True
        if x['size'] <= 9 and 'fold' not in x['operators']:
            solve_4(logger, cl, x)
            return True
    return False

def solve_3(pid, size, opers):
    assert size == 3
    assert len(opers) == 1
    code = '(lambda (x) (' + opers[0] + ' x))'
    p = parse(code)
    assert sz(p) == size
    assert ops(p) == frozenset(opers)
    return code

def solve_4(logger, cl, prob):
    pid = prob['id']
    vals = gen_vals()
    cl.evl(pid, vals)
    itr = 0
    while True:
        itr += 1
        if itr % 5000 == 0:
            logger('iter: %d\n' % itr)
        if itr > 1000000:
            break
        p = ['lambda', ['x_0'], gen_ast(prob['size'] - 1, prob['operators'], 1)]
        #logger('Trying: %s\n' % gen(p))
        if test(lambda x: None, cl, prob, p):
            logger('Found: %s\n' % gen(p))
            cl.guess(pid, gen(p))
            break

def gen_vals():
    vals = [0, 1, 2, 3, 4, 7, 8, 15, 16, 0xff, 0x100, 0x0102030405060708, 0xffffffffffffffff]
    while len(vals) < 256:
        vals.append(random.randrange(0, 0xffffffffffffffff + 1))
    return vals

def gen_ast(sz, ops, vs):
    if 'tfold' in ops:
        ops0 = [x for x in ops if ops != 'tfold']
        while True:
            try:
                res = ['fold', 'x_0', '0', ['lambda', ['x_0', 'x_1'], gen_ast0(sz - 4, ops0, vs + 1)[1]]]
                return res
            except:
                continue
    else:
        while True:
            try:
                res = gen_ast0(sz, ops, vs)
                return res[1]
            except:
                continue

def gen_ast0(sz, ops, vs):
    if sz < 1:
        raise Exception()
    my_ops = copy.deepcopy(ops)
    my_ops += ['const', 'var']
    op = random.choice(my_ops)
    if op == 'const':
        return sz - 1, random.choice(['0', '1'])
    elif op == 'var':
        return sz - 1, 'x_' + str(random.randrange(vs))
    elif op in ['not', 'shl1', 'shr1', 'shr4', 'shr16']:
        nsz, ast = gen_ast0(sz - 1, ops, vs)
        if nsz < 0:
            raise Exception()
        return nsz, [op, ast]
    elif op in ['and', 'or', 'xor', 'plus']:
        nsz, ast1 = gen_ast0(sz - 1, ops, vs)
        nsz, ast2 = gen_ast0(nsz, ops, vs)
        if nsz < 0:
            raise Exception()
        return nsz, [op, ast1, ast2]
    elif op == 'if0':
        nsz, ast1 = gen_ast0(sz - 1, ops, vs)
        nsz, ast2 = gen_ast0(nsz, ops, vs)
        nsz, ast3 = gen_ast0(nsz, ops, vs)
        if nsz < 0:
            raise Exception()
        return nsz, [op, ast1, ast2, ast3]
    assert False

def test(logger, cl, prob, p):
    assert valid(p)
    if sz(p) != prob['size']:
        logger('Size mismatch: %d vs. %s.\n' % (sz(p), prob['size']))
        return False
    if ops(p) != frozenset(prob['operators']):
        logger('Ops mismatch.\n')
        return False
    for k in prob['values']:
        logger('.')
        if prob['values'][k] != evl(p, k):
            logger('\nMismatch for %s: %s vs. %s.\n' % (hex(k), hex(prob['values'][k]), hex(evl(p, k))))
            return False
    logger('\n')
    logger('All ok!\n')
    return True

