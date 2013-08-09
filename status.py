
from client import Client

import sys

cl = Client(lambda x: sys.stderr.write(x))

cl.print_status()

