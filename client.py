
from secret import secret

import httplib
import json
import sys
import time

class Client:
    def __init__(self, logger = None):
        self.logger = logger
        if self.logger is None:
            self.logger = lambda x: None
        #if sys.executable[-4:] != 'pypy':
        #    self.logger('Whoa! You should be using pypy.\n')
        #    exit()

    def invoke(self, name, param):
        self.logger('Invoking %s...\n' % name)
        rq_body = json.dumps(param)
        cn = httplib.HTTPConnection('icfpc2013.cloudapp.net')
        cn.request('POST', '/' + name + '?auth=' + secret, rq_body)
        resp = cn.getresponse()
        if resp.status == 429:
            self.logger('Too many requests -- sleeping then repeating.\n')
            time.sleep(5)
            return self.invoke(name, param)
        raw = resp.read()
        data = None
        if raw is not None and raw != '':
            try:
                data = json.loads(raw)
            except ValueError:
                pass
        return resp.status, resp.reason, data

    def print_status(self):
        st, msg, resp = self.invoke('status', '')
        assert st == 200
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
        assert st == 200
        resp['operators'] = map(lambda x: x.encode('latin1'), resp['operators'])
        self.logger('\nStatus: %d\n' % st)
        self.logger('Reason: %s\n' % msg)
        self.logger('Response:\n')
        for k in resp:
            self.logger('%s: %s\n' % (k, str(resp[k])))
        self.logger('\n')
        return resp

    def myproblems(self):
        st, msg, resp = self.invoke('myproblems', '')
        assert st == 200
        self.logger('Total (live) problems: %d\n' % len(resp))
        resp.sort(key = lambda x: (x['timeLeft'] if 'timeLeft' in x else 1000, x['size']))
        for ix in range(len(resp)):
            resp[ix]['operators'] = map(lambda x: x.encode('latin1'), resp[ix]['operators'])
        return resp

    def guess(self, pid, code):
        st, msg, resp = self.invoke('guess', {'id': str(pid), 'program': str(code)})
        self.logger('\nStatus: %d\n' % st)
        self.logger('Reason: %s\n' % msg)
        if st == 200:
            self.logger('Response:\n')
            for k in resp:
                self.logger('%s: %s\n' % (k, str(resp[k])))
        self.logger('\n')
        if st == 412:
            return None
        return resp

    def evl(self, pid, xs):
        st, msg, resp = self.invoke('eval', {'id': pid, 'arguments': map(lambda x: x if x[-1] != 'L' else x[:-1], map(hex, xs))})
        self.logger('\nStatus: %d\n' % st)
        self.logger('Reason: %s\n' % msg)
        if st == 200:
            self.logger('Response:\n')
            for k in resp:
                if k == 'outputs':
                    continue
                self.logger('%s: %s\n' % (k, str(resp[k])))
        self.logger('\n')
        if st == 412:
            return None
        return resp

