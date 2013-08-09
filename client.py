
from secret import secret

import httplib
import json

class Client:
    def __init__(self, logger = None):
        self.logger = logger
        if self.logger is None:
            self.logger = lambda x: None

    def invoke(self, name, param):
        rq_body = json.dumps(param)
        cn = httplib.HTTPConnection('icfpc2013.cloudapp.net')
        cn.request('POST', '/' + name + '?auth=' + secret, rq_body)
        resp = cn.getresponse()
        raw = resp.read()
        data = None
        if raw is not None and raw != '':
            data = json.loads(raw)
        return resp.status, resp.reason, data

    def print_status(self):
        st, msg, resp = self.invoke('status', '')
        self.logger('\nStatus: %d\n' % st)
        self.logger('Reason: %s\n' % msg)
        self.logger('Response:\n')
        for k in resp:
            self.logger('%s: %s\n' % (k, str(resp[k])))
        self.logger('\n')

    def train(self, size = None, ops = None):
        if size is None and ops is None:
            args = ''
        else:
            args = {}
            if size is not None:
                args['size'] = size
            if ops is not None:
                args['operators'] = ops
        st, msg, resp = self.invoke('train', args)
        resp['operators'] = map(lambda x: x.encode('latin1'), resp['operators'])
        self.logger('Status: %d\n' % st)
        self.logger('Reason: %s\n' % msg)
        self.logger('Response:\n')
        for k in resp:
            self.logger('%s: %s\n' % (k, str(resp[k])))
        return resp

    def myproblems(self):
        st, msg, resp = self.invoke('myproblems', '')
        assert st == 200
        resp.sort(key = lambda x: x['size'])
        for ix in range(len(resp)):
            resp[ix]['operators'] = map(lambda x: x.encode('latin1'), resp[ix]['operators'])
        return resp

    def guess(self, pid, code):
        st, msg, resp = self.invoke('guess', {'id': str(pid), 'program': str(code)})
        self.logger('Status: %d\n' % st)
        self.logger('Reason: %s\n' % msg)
        self.logger('Response:\n')
        for k in resp:
            self.logger('%s: %s\n' % (k, str(resp[k])))
        return resp

    def evl(self, pid, xs):
        st, msg, resp = self.invoke('eval', {'id': pid, 'arguments': map(hex, xs)})
        self.logger('Status: %d\n' % st)
        self.logger('Reason: %s\n' % msg)
        self.logger('Response:\n')
        for k in resp:
            self.logger('%s: %s\n' % (k, str(resp[k])))
        return resp

