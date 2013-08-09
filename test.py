
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

process(resp)

cl.print_status()

