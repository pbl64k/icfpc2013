
from bv_parser import parse
from bv_meta import *
from bv import evl

import copy
import random

def process(logger, cl, resp, force = False):
    for x in resp:
        solved = 'solved' in x and x['solved']
        logger('size: %d ops: %s id: %s %s %s\n' % \
            (x['size'], str(x['operators']), x['id'], \
            ('SOLVED!' if solved else 'unsolved.'), \
            (('time:' + str(x['timeLeft'])) if 'timeLeft' in x and x['timeLeft'] > 0 else '')))
        if not force and (solved or ('timeLeft' in x and x['timeLeft'] == 0)):
            continue
        if x['size'] > 6:
            break
        if x['size'] == 3 and len(x['operators']) == 1:
            logger('\nSolving...\n')
            code = solve_3(x['id'], x['size'], x['operators'])
            logger(code + '\n')
            p = parse(code)
            logger(str(p) + '\n')
            logger(str(sz(p)) + '\n')
            logger(str(ops(p)) + '\n\n')
            cl.guess(x['id'], code)
            break
        if x['size'] <= 6 and 'if0' not in x['operators'] and 'tfold' not in x['operators'] and 'fold' not in x['operators']:
            solve_4(logger, cl, x)
            break

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
        if itr % 100 == 0:
            logger('iter: %d\n' % itr)
        if itr > 1000:
            break
        p = ['lambda', ['x_0'], gen_ast(prob['size'], prob['operators'], 1)]
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

