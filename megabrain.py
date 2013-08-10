
from bv_parser import parse
from bv_meta import *
from bv import evl
from gen_ast import *

import random

tabu_pid = None
tabu = set()

def process(logger, cl, resp, force = False):
    global tabu_pid, tabu
    for x in resp:
        solved = 'solved' in x and x['solved']
        if not solved:
            logger('size: %d ops: %s id: %s %s %s\n' % \
                (x['size'], str(x['operators']), x['id'], \
                ('SOLVED!' if solved else 'unsolved.'), \
                (('time: ' + str(x['timeLeft'])) if 'timeLeft' in x else '')))
        if not force and (solved or ('timeLeft' in x and x['timeLeft'] == 0)):
            continue
        if x['size'] > 17:
            return False, False
        #if x['size'] == 3 and len(x['operators']) == 1:
        #    logger('\nSolving...\n')
        #    code = solve_3(x['id'], x['size'], x['operators'])
        #    logger(code + '\n')
        #    p = parse(code)
        #    logger(str(p) + '\n')
        #    logger(str(sz(p)) + '\n')
        #    logger(str(ops(p)) + '\n\n')
        #    cl.guess(x['id'], code)
        #    return True, True
        if (x['size'] <= 13) or \
            (x['size'] <= 17 and 'tfold' in x['operators']):
            if tabu_pid != x['id']:
                logger('Blowing up the tabu list.\n')
                tabu_pid = x['id']
                tabu = set()
            success = solve_4(logger, cl, x)
            return True, success
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
        if itr > 500000:
            return False
        p = ['lambda', ['x_0'], gen_ast(prob['size'] - 1, prob['operators'], 1)]
        #logger('Trying: %s\n' % gen(p))
        #if test(logger, cl, prob, p):
        if test(lambda x: None, cl, prob, p):
            logger('Found: %s\n' % gen(p))
            return cl.guess(pid, gen(p))

def gen_vals():
    vals = [0, 1, 2, 3, 4, 7, 8, 15, 16, 0xff, 0x100, 0x0102030405060708, 0xffffffffffffffff]
    while len(vals) < 256:
        vals.append(random.randrange(0, 0xffffffffffffffff + 1))
    return vals

def test(logger, cl, prob, p, with_tabu = True):
    global tabu
    assert valid(p)
    gp = gen(p)
    #logger(gp + '\n')
    if with_tabu:
        if gp in tabu:
            return False
        tabu.add(gp)
    if sz(p) != prob['size']:
        logger('Size mismatch: %d vs. %s.\n' % (sz(p), prob['size']))
        return False
    if ops(p) != frozenset(prob['operators']):
        logger('Ops mismatch.\n')
        return False
    for k in prob['values']:
        logger('.')
        if prob['values'][k] != evl(p, k):
            #logger('\n')
            #logger(prob['challenge'] + '\n')
            #logger(gp + '\n')
            logger('\nMismatch for %s: %s vs. %s.\n' % (hex(k), hex(prob['values'][k]), hex(evl(p, k))))
            return False
    logger('\n')
    logger('All ok!\n')
    return True

