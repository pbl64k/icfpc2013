
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
    #cl.upd_problems()
    
    resp = cl.myproblems()
    
    process(logger, cl, resp)

with_cache(logger, main)

