
from cache import with_cache

from bv_parser import parse
from bv_meta import *
from bv import evl

from megabrain import *

import json
import os.path
import sys

def logger(s):
    sys.stdout.write(s)

def simple(x):
    return 'fold' not in x['operators'] \
        and 'tfold' not in x['operators'] \
        and 'if0' not in x['operators'] \
        and 'and' not in x['operators'] \
        and 'or' not in x['operators'] \
        and 'xor' not in x['operators'] \
        and 'plus' not in x['operators']

def less_simple(x):
    return 'fold' not in x['operators'] \
        and 'tfold' not in x['operators'] \
        and 'if0' not in x['operators']

def foldless(x):
    return 'fold' not in x['operators'] \
        and 'tfold' not in x['operators']

def simple_tfold(x):
    return 'fold' not in x['operators'] \
        and 'if0' not in x['operators'] \
        and 'and' not in x['operators'] \
        and 'or' not in x['operators'] \
        and 'xor' not in x['operators'] \
        and 'plus' not in x['operators']

def less_simple_tfold(x):
    return 'fold' not in x['operators'] \
        and 'if0' not in x['operators']

def main(cl):
    cl.upd_problems()
    resp = cl.myproblems()
    #disp(logger, cl, resp)
    #disp(logger, cl, resp, filt = simple)
    #disp(logger, cl, resp, filt = less_simple)
    #disp(logger, cl, resp, filt = foldless)
    #disp(logger, cl, resp, filt = simple_tfold)
    #disp(logger, cl, resp, filt = less_simple_tfold)
    disp(logger, cl, resp, filt = lambda x: x['size'] <= 20)

with_cache(logger, main)

