
from bv_parser import parse
from bv import evl

import sys

p = None

while True:
    sys.stdout.write(':> ')
    l = sys.stdin.readline()
    if len(l) == 0:
        break
    if len(l) == 1:
        continue
    try:
        if l[0] == '=':
            if p is None:
                sys.stdout.write('No function set.\n')
                continue
            s = l[1:]
            if s[0:2] == '0b':
                x = int(s[2:], 2)
            elif s[0:2] == '0x':
                x = int(s[2:], 16)
            else:
                x = int(s)
            z = evl(p, x)
            sys.stdout.write('Res: %d\n' % z)
            sys.stdout.write('Hex: %s\n' % hex(z))
            sys.stdout.write('Bin: %s\n' % bin(z))
        else:
            p = parse(l[:-1])
    except (AssertionError, ValueError) as ex:
        sys.stdout.write('Error.\n')
        raise

sys.stdout.write('\nThank you for playing.\n')

