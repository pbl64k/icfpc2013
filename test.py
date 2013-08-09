
from client import Client

from bv_parser import parse
from bv_meta import *
from bv import evl

from megabrain import *

import json

cl = Client()

#p = parse(u'(lambda (x_15083) (fold x_15083 0 (lambda (x_15083 x_15084) (if0 (shr4 (shr1 (or 1 x_15083))) x_15083 x_15084))))'.encode('latin1'))
#print evl(p, 0x0300001000000000)

resp = cl.myproblems()

for x in resp:
    print 'Size', x['size'], 'ops', x['operators'], x['id']
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

cl.print_status()

