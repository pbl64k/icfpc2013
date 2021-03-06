
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
    if t[0] != 'if0':
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

def is_if(x):
    return x[0] == 'if0'

def is_fold(x):
    return x[0] == 'fold'

def is_op1(x):
    return x[0] in ['not', 'shl1', 'shr1', 'shr4', 'shr16']

def is_op2(x):
    return x[0] in ['and', 'or', 'xor', 'plus']

def is_lambda(x):
    return x[0] == 'lambda'

def sz(t):
    if valid_const(t) or valid_ident(t):
        return 1
    #if valid_if(t):
    if is_if(t):
        return 1 + sz(t[1]) + sz(t[2]) + sz(t[3])
    #if valid_fold(t):
    if is_fold(t):
        return 2 + sz(t[1]) + sz(t[2]) + sz(t[3][2])
    #if valid_op1(t):
    if is_op1(t):
        return 1 + sz(t[1])
    #if valid_op2(t):
    if is_op2(t):
        return 1 + sz(t[1]) + sz(t[2])
    #if valid_lambda(t, 1) or valid_lambda(t, 2):
    if is_lambda(t):
        return 1 + sz(t[2])
    assert False

def op_expr(t):
    if valid_const(t) or valid_ident(t):
        return frozenset()
    #if valid_if(t):
    if is_if(t):
        return frozenset(['if0']) | op_expr(t[1]) | op_expr(t[2]) | op_expr(t[3])
    #if valid_fold(t):
    if is_fold(t):
        return frozenset(['fold']) | op_expr(t[1]) | op_expr(t[2]) | op_expr(t[3][2])
    #if valid_op1(t):
    if is_op1(t):
        return frozenset([t[0]]) | op_expr(t[1])
    #if valid_op2(t):
    if is_op2(t):
        return frozenset([t[0]]) | op_expr(t[1]) | op_expr(t[2])
    assert False

def ops(t):
    #assert valid(t)
    #if valid_fold(t[2]) and t[2][2] == '0':
    if isinstance(t[2], list) and t[2][0] == 'fold':
        return frozenset(['tfold']) | op_expr(t[2][3][2])
    return op_expr(t[2])

def gen(t):
    if isinstance(t, list):
        return '(' + ' '.join(map(gen, t)) + ')'
    return t

if __name__ == '__main__':
    assert valid_op2(parse('(or y z)'))
    assert valid(parse('(lambda (x) (fold x 0 (lambda (y z) (or y z))))'))
    assert sz(parse('(lambda (x) (fold x 0 (lambda (y z) (or y z))))')) == 8
    assert op_expr(parse('(fold x 0 (lambda (y z) (or y z)))')) == frozenset(['fold', 'or'])
    assert ops(parse('(lambda (x) (fold x 0 (lambda (y z) (or y z))))')) == frozenset(['tfold', 'or'])
    assert gen(parse('(lambda (x) (fold x 0 (lambda (y z) (or y z))))')) == '(lambda (x) (fold x 0 (lambda (y z) (or y z))))'

