
def parse(s):
    t = tokenize(s)
    tree, rem = parse0([], t + [')'])
    assert len(rem) == 0
    assert len(tree) == 1
    return tree[0]

def parse0(acc, ts):
    assert len(ts) > 0
    t = ts[0]
    ts = ts[1:]
    if t == ')':
        return acc, ts
    elif t == '(':
        tree, rem = parse0([], ts)
        acc.append(tree)
        return parse0(acc, rem)
    else:
        acc.append(t)
        return parse0(acc, ts)

def tokenize(s):
    return tokenize0([], '', s)

def add_token(acc, t):
    if len(t) > 0:
        acc.append(t)

def tokenize0(acc, t, s):
    if len(s) == 0:
        add_token(acc, t)
        return acc
    c = s[0]
    s = s[1:]
    if c == ' ':
        add_token(acc, t)
        t = ''
    elif c == '(' or c == ')':
        add_token(acc, t)
        add_token(acc, c)
        t = ''
    else:
        t += c
    return tokenize0(acc, t, s)

if __name__ == '__main__':
    assert tokenize('(lambda (x) (fold x 0 (lambda (y z) (or y z))))') == \
        ['(', 'lambda', '(', 'x', ')', '(', 'fold', 'x', '0', '(', 'lambda', '(', 'y', 'z', ')', '(', 'or', 'y', 'z', ')', ')', ')', ')']
    assert parse('(lambda (x) (fold x 0 (lambda (y z) (or y z))))') == \
        ['lambda', ['x'], ['fold', 'x', '0', ['lambda', ['y', 'z'], ['or', 'y', 'z']]]]

