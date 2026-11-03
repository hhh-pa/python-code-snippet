import sys

sys.setrecursionlimit(200000)

class Ty:
    def __init__(self, kind, id_val=0, name="", l=None, r=None):
        self.kind = kind  # 0: var, 1: con, 2: arrow
        self.id = id_val
        self.name = name
        self.l = l
        self.r = r

def TVar(vid):
    return Ty(0, id_val=vid)

def TCon(name):
    return Ty(1, name=name)

def TArr(a, b):
    return Ty(2, l=a, r=b)

def applyS(s, t):
    if t.kind == 0:
        if t.id in s:
            return applyS(s, s[t.id])
        return t
    if t.kind == 1:
        return t
    return TArr(applyS(s, t.l), applyS(s, t.r))

def ftv(t, out):
    if t.kind == 0:
        out.add(t.id)
    elif t.kind == 2:
        ftv(t.l, out)
        ftv(t.r, out)

def occurs(v, t):
    s = set()
    ftv(t, s)
    return v in s

def compS(s1, s2):
    r = {k: applyS(s1, v) for k, v in s2.items()}
    for k, v in s1.items():
        if k not in r:
            r[k] = v
    return r

def unify(a, b, s):
    a = applyS(s, a)
    b = applyS(s, b)
    if a.kind == 0:
        if b.kind == 0 and a.id == b.id:
            return s.copy(), True
        if occurs(a.id, b):
            return None, False
        out = s.copy()
        out[a.id] = b
        return out, True
    if b.kind == 0:
        if occurs(b.id, a):
            return None, False
        out = s.copy()
        out[b.id] = a
        return out, True
    if a.kind == 1 and b.kind == 1:
        if a.name != b.name:
            return None, False
        return s.copy(), True
    if a.kind == 2 and b.kind == 2:
        s1, ok = unify(a.l, b.l, s)
        if not ok:
            return None, False
        return unify(a.r, b.r, s1)
    return None, False

class Ex:
    def __init__(self, kind, atom="", var="", a=None, b=None, c=None):
        self.kind = kind  # 0: atom, 1: lam, 2: app, 3: let, 4: if, 5: binop
        self.atom = atom
        self.var = var
        self.a = a
        self.b = b
        self.c = c

class Parser:
    def __init__(self, s):
        self.s = s
        self.p = 0
        self.bad = False

    def sp(self):
        while self.p < len(self.s) and self.s[self.p] in ' \t\r\n':
            self.p += 1

    def atom(self):
        self.sp()
        q = self.p
        while q < len(self.s) and self.s[q] not in ' \t\r\n()':
            q += 1
        r = self.s[self.p:q]
        self.p = q
        return r

    def expr(self):
        self.sp()
        if self.p >= len(self.s):
            self.bad = True
            return None
        if self.s[self.p] == '(':
            self.p += 1
            self.sp()
            kw = self.atom()
            if kw == "lam":
                self.sp()
                v = self.atom()
                b = self.expr()
                self.sp()
                if self.p >= len(self.s) or self.s[self.p] != ')':
                    self.bad = True
                    return None
                self.p += 1
                return Ex(1, var=v, a=b)
            if kw == "app":
                f = self.expr()
                x = self.expr()
                self.sp()
                if self.p >= len(self.s) or self.s[self.p] != ')':
                    self.bad = True
                    return None
                self.p += 1
                return Ex(2, a=f, b=x)
            if kw == "let":
                self.sp()
                v = self.atom()
                val = self.expr()
                bo = self.expr()
                self.sp()
                if self.p >= len(self.s) or self.s[self.p] != ')':
                    self.bad = True
                    return None
                self.p += 1
                return Ex(3, var=v, a=val, b=bo)
            if kw == "if":
                c = self.expr()
                t = self.expr()
                e = self.expr()
                self.sp()
                if self.p >= len(self.s) or self.s[self.p] != ')':
                    self.bad = True
                    return None
                self.p += 1
                return Ex(4, a=c, b=t, c=e)
            if kw in ("+", "=="):
                x = self.expr()
                y = self.expr()
                self.sp()
                if self.p >= len(self.s) or self.s[self.p] != ')':
                    self.bad = True
                    return None
                self.p += 1
                return Ex(5, atom=kw, a=x, b=y)
            self.bad = True
            return None
        a = self.atom()
        if not a:
            self.bad = True
            return None
        return Ex(0, atom=a)

class Scheme:
    def __init__(self, qs, t):
        self.qs = qs
        self.t = t

freshc = 0
def fresh():
    global freshc
    v = freshc
    freshc += 1
    return TVar(v)

def ftvEnv(env, out):
    for sc in env.values():
        s = set()
        ftv(sc.t, s)
        qs_set = set(sc.qs)
        for v in s:
            if v not in qs_set:
                out.add(v)

def inst(sc):
    s = {}
    for v in sc.qs:
        s[v] = fresh()
    return applyS(s, sc.t)

def gen(env, t):
    a = set()
    b = set()
    ftv(t, a)
    ftvEnv(env, b)
    qs = [v for v in a if v not in b]
    return Scheme(qs, t)

def applyEnv(s, env):
    return {k: Scheme(sc.qs, applyS(s, sc.t)) for k, sc in env.items()}

def infer(env, e):
    if e.kind == 0:
        a = e.atom
        if a.isdigit():
            return {}, TCon("int"), True
        if a in ("T", "F"):
            return {}, TCon("bool"), True
        if a not in env:
            return None, None, False
        return {}, inst(env[a]), True
    if e.kind == 1:
        b = fresh()
        e2 = dict(env)
        e2[e.var] = Scheme([], b)
        s1, t1, ok = infer(e2, e.a)
        if not ok:
            return None, None, False
        return s1, TArr(applyS(s1, b), t1), True
    if e.kind == 2:
        s1, t1, ok = infer(env, e.a)
        if not ok:
            return None, None, False
        e2 = applyEnv(s1, env)
        s2, t2, ok = infer(e2, e.b)
        if not ok:
            return None, None, False
        b = fresh()
        u1 = applyS(s2, t1)
        u2 = TArr(t2, b)
        s3, ok = unify(u1, u2, {})
        if not ok:
            return None, None, False
        t12 = compS(s2, s1)
        return compS(s3, t12), applyS(s3, b), True
    if e.kind == 3:
        s1, t1, ok = infer(env, e.a)
        if not ok:
            return None, None, False
        e2 = applyEnv(s1, env)
        sc = gen(e2, t1)
        e2[e.var] = sc
        s2, t2, ok = infer(e2, e.b)
        if not ok:
            return None, None, False
        return compS(s2, s1), t2, True
    if e.kind == 4:
        s1, tc, ok = infer(env, e.a)
        if not ok:
            return None, None, False
        sa, ok = unify(tc, TCon("bool"), s1)
        if not ok:
            return None, None, False
        e2 = applyEnv(sa, env)
        s2, tt, ok = infer(e2, e.b)
        if not ok:
            return None, None, False
        e3 = applyEnv(s2, e2)
        s3, te, ok = infer(e3, e.c)
        if not ok:
            return None, None, False
        u1 = applyS(s3, tt)
        sb, ok = unify(u1, te, {})
        if not ok:
            return None, None, False
        t1 = compS(s3, s2)
        t2 = compS(t1, sa)
        return compS(sb, t2), applyS(sb, te), True
    if e.kind == 5:
        s1, t1, ok = infer(env, e.a)
        if not ok:
            return None, None, False
        sa, ok = unify(t1, TCon("int"), s1)
        if not ok:
            return None, None, False
        e2 = applyEnv(sa, env)
        s2, t2, ok = infer(e2, e.b)
        if not ok:
            return None, None, False
        sb, ok = unify(t2, TCon("int"), s2)
        if not ok:
            return None, None, False
        c1 = compS(sb, s2)
        c2 = compS(c1, sa)
        ret_ty = TCon("int") if e.atom == "+" else TCon("bool")
        return compS(c2, s1), ret_ty, True
    return None, None, False

def collect(t, out):
    if t.kind == 0:
        if t.id not in out:
            out.append(t.id)
    elif t.kind == 2:
        collect(t.l, out)
        collect(t.r, out)

def showT(t, nm):
    if t.kind == 0:
        return nm[t.id]
    if t.kind == 1:
        return t.name
    return f"({showT(t.l, nm)} -> {showT(t.r, nm)})"

def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx >= len(lines):
        return
    try:
        T = int(lines[idx].strip())
    except ValueError:
        return
    idx += 1

    global freshc
    out = []
    for _ in range(T):
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        if idx >= len(lines):
            out.append("HM TYPE-ERROR")
            continue
        line = lines[idx].strip()
        idx += 1

        ps = Parser(line)
        e = ps.expr()
        ps.sp()
        if ps.bad or e is None or ps.p != len(line):
            out.append("HM TYPE-ERROR")
            continue

        freshc = 0
        s, t, ok = infer({}, e)
        if not ok:
            out.append("HM TYPE-ERROR")
            continue
        f = applyS(s, t)
        vs = []
        collect(f, vs)
        nm = {vid: chr(ord('a') + i) for i, vid in enumerate(vs)}
        out.append(f"HM {showT(f, nm)}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
