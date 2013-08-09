
from bv_parser import parse
from bv_meta import *
from bv import evl

def process(resp):
    for x in resp:
        solved = 'solved' in x and x['solved']
        print 'size:', x['size'], 'ops:', x['operators'], 'id:', x['id'], ('SOLVED!' if solved else 'unsolved.')
        if solved:
            continue
        if x['size'] == 3 and len(x['operators']) == 1:
            print
            print 'Solving...'
            code = solve_3(x['id'], x['size'], x['operators'])
            print code
            p = parse(code)
            print p
            print sz(p)
            print ops(p)
            print
            cl.guess(x['id'], code)
            break
        if x['size'] > 4:
            break

def solve_3(pid, size, opers):
    assert size == 3
    assert len(opers) == 1
    code = '(lambda (x) (' + opers[0] + ' x))'
    p = parse(code)
    assert sz(p) == size
    assert ops(p) == frozenset(opers)
    return code

