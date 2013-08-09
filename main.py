
from cache import with_cache

from bv_parser import parse
from bv_meta import *
from bv import evl

from megabrain import *

import json
import sys

def logger(s):
    sys.stderr.write(s)

def main(cl):
    while True:
        cl.upd_problems()
        resp = cl.myproblems()
        res = process(logger, cl, resp)
        if not res:
            logger('Done.\n')
            break

with_cache(logger, main)

