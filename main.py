
from cache import with_cache

from bv_parser import parse
from bv_meta import *
from bv import evl

from megabrain import *

import json
import os.path
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
        try:
            os.path.exists('./x')
            break
        except IOError:
            continue

with_cache(logger, main)

