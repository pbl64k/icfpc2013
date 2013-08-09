
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
    pid = cl.train(4)
    process(logger, cl, [cl.problems[pid]], True)

with_cache(logger, main)

