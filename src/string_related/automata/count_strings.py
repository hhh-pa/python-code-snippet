import sys

MOD = 1000000007

# AST types: 'char', 'concat', 'union', 'star'

class AST:
    __slots__ = ('kind', 'ch', 'left', 'right', 'kids')
    def __init__(self, kind, ch=0, left=None, right=None, kids=None):
        self.kind = kind
        self.ch = ch
        self.left = left
        self.right = right
        self.kids = kids if kids is not None else []

class Parser:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.n = len(s)

    def peek(self):
        if self.i >= self.n:
            return ''
        return self.s[self.i]

    def eat(self):
        c = self.peek()
        if c:
            self.i += 1
        return c

    def parse(self):
        return self.parse_expr()

    def parse_expr(self):
        node = self.parse_term()
        while self.peek() == '|':
            self.eat()
            rhs = self.parse_term()
            node = AST('union', left=node, right=rhs)
        return node

    def parse_term(self):
        parts = []
        while True:
            c = self.peek()
            if not c or c == ')' or c == '|':
                break
            parts.append(self.parse_factor())
        if len(parts) == 1:
            return parts[0]
        return AST('concat', kids=parts)

    def parse_factor(self):
        node = self.parse_atom()
        while self.peek() == '*':
            self.eat()
            node = AST('star', left=node)
        return node

    def parse_atom(self):
        c = self.eat()
        if c == 'a':
            return AST('char', ch=1)
        elif c == 'b':
            return AST('char', ch=2)
        elif c == '(':
            node = self.parse_expr()
            self.eat()  # eat ')'
            return node
        else:
            raise ValueError(f"unexpected char {c}")

class NFA:
    def __init__(self):
        self.adj = []

    def new_state(self):
        idx = len(self.adj)
        self.adj.append([])
        return idx

    def add_edge(self, u, v, lab):
        self.adj[u].append((v, lab))

def build_nfa(a, nfa):
    start = nfa.new_state()
    end = nfa.new_state()
    if a.kind == 'char':
        nfa.add_edge(start, end, a.ch)
    elif a.kind == 'concat':
        if not a.kids:
            nfa.add_edge(start, end, 0)
        else:
            prev = -1
            for k in a.kids:
                i, o = build_nfa(k, nfa)
                if prev == -1:
                    nfa.add_edge(start, i, 0)
                else:
                    nfa.add_edge(prev, i, 0)
                prev = o
            nfa.add_edge(prev, end, 0)
    elif a.kind == 'union':
        li, lo = build_nfa(a.left, nfa)
        ri, ro = build_nfa(a.right, nfa)
        nfa.add_edge(start, li, 0)
        nfa.add_edge(start, ri, 0)
        nfa.add_edge(lo, end, 0)
        nfa.add_edge(ro, end, 0)
    elif a.kind == 'star':
        ii, io = build_nfa(a.left, nfa)
        nfa.add_edge(start, ii, 0)
        nfa.add_edge(start, end, 0)
        nfa.add_edge(io, ii, 0)
        nfa.add_edge(io, end, 0)
    return start, end

def eclosure_set(nfa, starts):
    seen = [False] * len(nfa.adj)
    q = []
    for s in starts:
        if not seen[s]:
            seen[s] = True
            q.append(s)
    head = 0
    while head < len(q):
        u = q[head]
        head += 1
        for v, lab in nfa.adj[u]:
            if lab == 0 and not seen[v]:
                seen[v] = True
                q.append(v)
    return tuple(i for i, ok in enumerate(seen) if ok)

def move_set(nfa, states, lab):
    hs = set()
    for u in states:
        for v, elab in nfa.adj[u]:
            if elab == lab:
                hs.add(v)
    return sorted(hs)

def mat_mul(a, b):
    n = len(a)
    r = [[0] * n for _ in range(n)]
    for i in range(n):
        ai = a[i]
        ri = r[i]
        for k in range(n):
            aik = ai[k]
            if aik == 0:
                continue
            bk = b[k]
            for j in range(n):
                bkj = bk[j]
                if bkj != 0:
                    ri[j] = (ri[j] + aik * bkj) % MOD
    return r

def mat_pow(m, p):
    n = len(m)
    r = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = m
    while p > 0:
        if p & 1:
            r = mat_mul(r, base)
        p >>= 1
        if p > 0:
            base = mat_mul(base, base)
    return r

def count_strings(regex, l):
    p = Parser(regex)
    a = p.parse()
    nfa = NFA()
    start_nfa, end_nfa = build_nfa(a, nfa)

    start_set = eclosure_set(nfa, [start_nfa])
    states = [start_set]
    id_map = {start_set: 0}
    dfa_adj = []
    q = [0]
    head = 0

    while head < len(q):
        cur = q[head]
        head += 1
        while cur >= len(dfa_adj):
            dfa_adj.append([0, 0])
        cur_set = states[cur]

        for idx, lab in enumerate((1, 2)):
            moved = move_set(nfa, cur_set, lab)
            to = eclosure_set(nfa, moved) if moved else ()
            if to not in id_map:
                nxt = len(states)
                states.append(to)
                id_map[to] = nxt
                q.append(nxt)
            else:
                nxt = id_map[to]
            dfa_adj[cur][idx] = nxt

    while len(dfa_adj) < len(states):
        dfa_adj.append([0, 0])

    end_states = []
    for i, st in enumerate(states):
        if end_nfa in st:
            end_states.append(i)

    sz = len(states)
    mat = [[0] * sz for _ in range(sz)]
    for i in range(sz):
        mat[i][dfa_adj[i][0]] = (mat[i][dfa_adj[i][0]] + 1) % MOD
        mat[i][dfa_adj[i][1]] = (mat[i][dfa_adj[i][1]] + 1) % MOD

    mp = mat_pow(mat, l)
    ans = 0
    row0 = mp[0]
    for e in end_states:
        ans = (ans + row0[e]) % MOD
    return ans

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    t = int(next(it))
    out = []
    for _ in range(t):
        r = next(it)
        l = int(next(it))
        out.append(str(count_strings(r, l)))
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
