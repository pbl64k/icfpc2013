
from client import Client

from bv_parser import parse
from bv import evl

import json

cl = Client()

#st, msg, resp = cl.invoke('status', '')
#
#print 'Status:', st
#print 'Reason:', msg
#print 'Response:', json.dumps(resp)
#
#st, msg, resp = cl.invoke('train', '')
#
#print 'Status:', st
#print 'Reason:', msg
#print 'Response:', resp

p = parse(u'(lambda (x_15083) (fold x_15083 0 (lambda (x_15083 x_15084) (if0 (shr4 (shr1 (or 1 x_15083))) x_15083 x_15084))))'.encode('latin1'))
print evl(p, 0x0300001000000000)

