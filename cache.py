
from client import Client

from bv_parser import parse
from bv_meta import *
from bv import evl

from megabrain import *

import json
import pickle
import sys

class Cache:
    def __init__(self, logger = None):
        self.logger = logger
        if self.logger is None:
            self.logger = lambda x: None
        self.cl = Client(self.logger)
        #self.problems = {}
        self.problems = pickle.load(open('./problems.dat'))

    def save(self):
        self.logger('Saving...\n')
        pickle.dump(self.problems, open('./problems.dat', 'w'))

    def upd_problems(self):
        self.logger('Updating problems...\n')
        resp = self.cl.myproblems()
        for prob in resp:
            pid = prob['id']
            if pid in self.problems:
                for k in prob:
                    self.problems[pid][k] = prob[k]
            else:
                self.problems[pid] = prob

    def myproblems(self):
        r = self.problems.values()
        r.sort(key = lambda x: (x['timeLimit'] if 'timeLimit' in x else 1000, x['size']))
        return r

    def guess(self, pid, code):
        assert pid in self.problems
        if 'guesses' not in self.problems[pid]:
            self.problems[pid]['guesses'] = []
        self.problems[pid]['guesses'].append(code)
        res = self.cl.guess(pid, code)
        if res['status'] == 'win':
            self.logger('\n********** WIN **********\n\n')
            self.problems[pid]['solved'] = True
            self.save()
            return True
        self.logger('\n---------- BOO ----------\n\n')
        if 'values' in res:
            x, f, m = map(lambda x: int(x[2:], 16), res['values'])
            if 'values' not in self.problems[pid]:
                self.problems[pid]['values'] = {}
            self.problems[pid]['values'][x] = f
            self.save()
        return False

    def evl(self, pid, xs):
        assert pid in self.problems
        res = self.cl.evl(pid, xs)
        if res['status'] != 'ok':
            return
        for x, f in zip(xs, res['outputs']):
            f0 = int(f[2:], 16)
            if 'values' not in self.problems[pid]:
                self.problems[pid]['values'] = {}
            self.problems[pid]['values'][x] = f0
        self.save()

    def train(self, size = None, ops = None):
        res = self.cl.train(size, ops)
        self.problems[res['id']] = res
        self.problems[res['id']]['solved'] = True
        self.problems[res['id']]['training'] = True
        return res['id']

def with_cache(logger, f):
    cl = Cache(logger)

    f(cl)

    cl.save()

if __name__ == '__main__':
    c = Cache(lambda x: sys.stderr.write(x))
    c.upd_problems()
    c.save()

