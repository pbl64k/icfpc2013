
from bv_parser import parse
from bv_meta import *
from bv import evl

def process(logger, cl, resp, force = False):
    for x in resp:
        solved = 'solved' in x and x['solved']
        logger('size: %d ops: %s id: %s %s %s\n' % \
            (x['size'], str(x['operators']), x['id'], \
            ('SOLVED!' if solved else 'unsolved.'), \
            (('time:' + str(x['timeLeft'])) if 'timeLeft' in x and x['timeLeft'] > 0 else '')))
        if not force and (solved or ('timeLeft' in x and x['timeLeft'] == 0)):
            continue
        if x['size'] > 4:
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

def solve_3(pid, size, opers):
    assert size == 3
    assert len(opers) == 1
    code = '(lambda (x) (' + opers[0] + ' x))'
    p = parse(code)
    assert sz(p) == size
    assert ops(p) == frozenset(opers)
    return code

