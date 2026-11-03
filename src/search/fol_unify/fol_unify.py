import sys

class Term:
    __slots__ = ('sym', 'args', 'isvar')
    def __init__(self, sym, args=None, isvar=False):
        self.sym = sym
        self.args = args if args is not None else []
        self.isvar = isvar

def parse_term(s, pos):
    q = pos
    n = len(s)
    while q < n and (s[q].isalnum() or s[q] == '_'):
        q += 1
    sym = s[pos:q]
    pos = q
    if pos < n and s[pos] == '(':
        pos += 1
        args = []
        while True:
            arg, pos = parse_term(s, pos)
            args.append(arg)
            if s[pos] == ',':
                pos += 1
                continue
            pos += 1  # skip ')'
            break
        return Term(sym, args, False), pos
    isvar = sym[0].islower()
    return Term(sym, [], isvar), pos

def show(t):
    if not t.args:
        return t.sym
    return f"{t.sym}({','.join(show(a) for a in t.args)})"

def subst(t, th):
    if t.isvar:
        if t.sym not in th:
            return t
        r = subst(th[t.sym], th)
        th[t.sym] = r
        return r
    a = [subst(x, th) for x in t.args]
    return Term(t.sym, a, False)

def occurs(v, t, th):
    s = subst(t, th)
    if s.isvar:
        return s.sym == v
    for x in s.args:
        if occurs(v, x, th):
            return True
    return False

def unify(a, b, th):
    a = subst(a, th)
    b = subst(b, th)
    if a.isvar and b.isvar and a.sym == b.sym:
        return True
    if a.isvar:
        if occurs(a.sym, b, th):
            return False
        th[a.sym] = b
        return True
    if b.isvar:
        if occurs(b.sym, a, th):
            return False
        th[b.sym] = a
        return True
    if a.sym != b.sym or len(a.args) != len(b.args):
        return False
    for i in range(len(a.args)):
        if not unify(a.args[i], b.args[i], th):
            return False
    return True

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    
    try:
        T_str = next(it)
    except StopIteration:
        return
    T = int(T_str)
    
    out = []
    for _ in range(T):
        s1 = next(it)
        s2 = next(it)
        t1, _ = parse_term(s1, 0)
        t2, _ = parse_term(s2, 0)
        th = {}
        ok = unify(t1, t2, th)
        if not ok:
            out.append("UNIFY FAIL")
        else:
            keys = sorted(th.keys())
            row = ["UNIFY"]
            for k in keys:
                val_str = show(subst(th[k], th))
                row.append(f"{k}={val_str}")
            out.append(" ".join(row))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
