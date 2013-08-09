
from client import Client

import json

cl = Client()

st, msg, resp = cl.invoke('status', '')

print 'Status:', st
print 'Reason:', msg
print 'Response:', json.dumps(resp)

