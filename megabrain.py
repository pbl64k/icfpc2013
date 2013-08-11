
from bv_parser import parse
from bv_meta import *
from bv import evl
from gen_ast import *
from model import *

import random
import sys

tabu_pid = None
tabu = set()

maxsize = 16
maxsize_tfold = 16
maxsize_fold = 13
maxsize_model = 10

def process(logger, cl, resp, force = False):
    global tabu_pid, tabu
    global maxsize, maxsize_tfold, maxsize_fold, maxsize_model
    busted = 0
    #exit()
    for x in resp:
        solved = 'solved' in x and x['solved']
        if 'timeLeft' in x and x['timeLeft'] == 0:
            if not solved:
                busted += 1
        elif busted >= 0:
            logger('Problems busted %d\n' % busted)
            busted = -1
        if not solved:
            logger('size: %d ops: %s id: %s %s %s\n' % \
                (x['size'], str(x['operators']), x['id'], \
                ('SOLVED!' if solved else 'unsolved.'), \
                (('time: ' + str(x['timeLeft'])) if 'timeLeft' in x else '')))
        if not force and (solved or ('timeLeft' in x and x['timeLeft'] == 0)):
            continue
        if x['size'] > max(maxsize, maxsize_tfold):
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
        if 'bonus' not in x['operators'] \
            and 'fold' not in x['operators'] \
            and 'tfold' not in x['operators'] \
            and (x['size'] <= maxsize_model):
            pid = x['id']
            vals = gen_vals(False)
            cl.evl(pid, vals)
            success = solve_model(logger, cl, x['size'], x['operators'], cl.problems[pid]['values'], x['id'])
            exit()
            return True, success
        if 'bonus' not in x['operators'] \
            and ((x['size'] <= maxsize and 'fold' not in x['operators'] and not 'tfold' in x['operators']) \
            or (x['size'] <= maxsize_fold) \
            or (x['size'] <= maxsize_tfold and 'tfold' in x['operators'])):
            if tabu_pid != x['id']:
                logger('Blowing up the tabu list.\n')
                tabu_pid = x['id']
                tabu = set()
            success = solve_4(logger, cl, x)
            return True, success
        #if (x['size'] <= maxsize) or (x['size'] <= maxsize_tfold and 'tfold' in x['operators']):
        #    success = solve_ts(logger, cl, x)
        #    return True, success
    return False

def disp(logger, cl, resp, filt = None):
    if filt is None:
        filt = lambda x: True
    for x in resp:
        if filt(x):
            solved = 'solved' in x and x['solved']
            logger('size: %d ops: %s id: %s %s %s\n' % \
                (x['size'], str(x['operators']), x['id'], \
                ('SOLVED!' if solved else 'unsolved.'), \
                (('time: ' + str(x['timeLeft'])) if 'timeLeft' in x else '')))

def solve_3(pid, size, opers):
    assert size == 3
    assert len(opers) == 1
    code = '(lambda (x) (' + opers[0] + ' x))'
    p = parse(code)
    assert sz(p) == size
    assert ops(p) == frozenset(opers)
    return code

def solve_4(logger, cl, prob):
    if sys.executable[-4:] != 'pypy':
        self.logger('Whoa! You should be using pypy.\n')
        exit()
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
        # do a switcheroo?
        p = ['lambda', ['x_0'], gen_ast(prob['size'] - 1, prob['operators'], 1)]
        #logger('Trying: %s\n' % gen(p))
        #if test(logger, cl, prob, p):
        if test(lambda x: None, cl, prob, p):
            logger('Found: %s\n' % gen(p))
            return cl.guess(pid, gen(p))

def solve_ts(logger, cl, prob):
    if sys.executable[-4:] != 'pypy':
        self.logger('Whoa! You should be using pypy.\n')
        exit()
    pid = prob['id']
    vals = gen_vals()
    cl.evl(pid, vals)
    itr = 0
    for p in itr_ast(prob['size'], prob['operators']):
        itr += 1
        if itr % 100000 == 0:
            logger('iter: %d\n' % itr)
        if test(lambda x: None, cl, prob, p, False):
            logger('Found: %s\n' % gen(p))
            res = cl.guess(pid, gen(p))
            if res:
                return res
            else:
                vals = gen_vals(False)
                cl.evl(pid, vals)

def gen_vals(init = True):
    if init:
        vals = [0, 1, 2, 3, 4, 7, 8, 15, 16, 0xff, 0x100, 0x0102030405060708, 0xffffffffffffffff]
    else:
        vals = []
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
    #if sz(p) != prob['size']:
    if sz(p) > prob['size']:
        logger('Size mismatch: %d vs. %s.\n' % (sz(p), prob['size']))
        return False
    #if ops(p) != frozenset(prob['operators']):
    #    logger('Ops mismatch.\n')
    #    return False
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

