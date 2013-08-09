
from bv_parser import parse

import re

def valid(t):
    return valid_lambda(t, 1)

def valid_lambda(t, l):
    if not isinstance(t, list):
        return False
    if t[0] != 'lambda':
        return False
    if len(t) != 3:
        return False
    if len(t[1]) != l:
        return False
    if not all(map(valid_ident, t[1])):
        return False
    if not valid_expr(t[2]):
        return False
    return True

def valid_expr(t):
    if valid_const(t):
        return True
    if valid_ident(t):
        return True
    if valid_if(t):
        return True
    if valid_fold(t):
        return True
    if valid_op1(t):
        return True
    if valid_op2(t):
        return True
    return False

def valid_const(t):
    return isinstance(t, str) and (t in ['0', '1'])

def valid_if(t):
    if not isinstance(t, list):
        return False
    if len(t) != 4:
        return False
    if t[0] != 'if':
        return False
    if not valid_expr(t[1]):
        return False
    if not valid_expr(t[2]):
        return False
    if not valid_expr(t[3]):
        return False
    return True

def valid_fold(t):
    if not isinstance(t, list):
        return False
    if len(t) != 4:
        return False
    if t[0] != 'fold':
        return False
    if not valid_expr(t[1]):
        return False
    if not valid_expr(t[2]):
        return False
    if not valid_lambda(t[3], 2):
        return False
    return True

def valid_op1(t):
    if not isinstance(t, list):
        return False
    if len(t) != 2:
        return False
    if t[0] not in ['not', 'shl1', 'shr1', 'shr4', 'shr16']:
        return False
    if not valid_expr(t[1]):
        return False
    return True

def valid_op2(t):
    if not isinstance(t, list):
        return False
    if len(t) != 3:
        return False
    if t[0] not in ['and', 'or', 'xor', 'plus']:
        return False
    if not valid_expr(t[1]):
        return False
    if not valid_expr(t[2]):
        return False
    return True

def valid_ident(t):
    return isinstance(t, str) and re.match('^[a-z][a-z_0-9]*$', t)

if __name__ == '__main__':
    assert valid_op2(parse('(or y z)')) == True
    assert valid(parse('(lambda (x) (fold x 0 (lambda (y z) (or y z))))')) == True

