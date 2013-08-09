
from secret import secret

import httplib
import json

class Client:
    def __init__(self):
        pass

    def invoke(self, name, param):
        rq_body = json.dumps(param)
        cn = httplib.HTTPConnection('icfpc2013.cloudapp.net')
        cn.request('POST', '/' + name + '?auth=' + secret, rq_body)
        resp = cn.getresponse()
        data = json.loads(resp.read())
        return resp.status, resp.reason, data

    def print_status(self):
        st, msg, resp = self.invoke('status', '')
        print
        print 'Status:', st
        print 'Reason:', msg
        print 'Response:'
        for k in resp:
            print '%s: %s' % (k, str(resp[k]))
        print

    def train(self):
        #st, msg, resp = self.invoke('train', '')
        #print 'Status:', st
        #print 'Reason:', msg
        #print 'Response:', resp
        pass

    def myproblems(self):
        st, msg, resp = self.invoke('myproblems', '')
        assert st == 200
        resp.sort(key = lambda x: x['size'])
        for ix in range(len(resp)):
            resp[ix]['operators'] = map(lambda x: x.encode('latin1'), resp[ix]['operators'])
        return resp

    def guess(self, pid, code):
        st, msg, resp = self.invoke('guess', {'id': str(pid), 'program': str(code)})
        print 'Status:', st
        print 'Reason:', msg
        print 'Response:'
        for k in resp:
            print '%s: %s' % (k, str(resp[k]))
        return resp

