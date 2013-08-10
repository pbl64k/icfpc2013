
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
    #pid = 'XBNFlPyaUmj7ANFcZADEZQDh'
    #pid = 'UxfT5ySTPIbkArFkVhmd1IUC'
    #pid = cl.train(17, ['tfold'])
    #pid = cl.train(13, ['fold'])
    pid = cl.train(13, [])
    process(logger, cl, [cl.problems[pid]], True)

with_cache(logger, main)

