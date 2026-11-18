"""LALR(1) table construction + parsing (Louden 5.4.3)."""

import sys


def _first_add(first, lhs, rhs):
    if not rhs:
        if None not in first[lhs]:
            first[lhs].add(None)
            return True
        return False
    changed = False
    for s in rhs:
        if s not in first:
            if s not in first[lhs]:
                first[lhs].add(s)
                changed = True
            return changed
        before = len(first[lhs])
        first[lhs] |= first[s] - {None}
        if len(first[lhs]) != before:
            changed = True
        if None not in first[s]:
            return changed
    if None not in first[lhs]:
        first[lhs].add(None)
        changed = True
    return changed


def _first_sets(prods):
    first = {}
    for lhs, _ in prods:
        first.setdefault(lhs, set())
    changed = True
    while changed:
        changed = False
        for lhs, rhs in prods:
            changed |= _first_add(first, lhs, rhs)
    return first


def _first_seq(first, seq):
    out = set()
    for s in seq:
        if s not in first:
            out.add(s)
            return out, False
        out |= first[s] - {None}
        if None not in first[s]:
            return out, False
    return out, True


def _closure(prods, items, first):
    out = dict(items)
    work = list(items)
    while work:
        p, d, la = work.pop()
        _lhs, rhs = prods[p]
        if d < len(rhs) and rhs[d] in first:
            b = rhs[d]
            fset, _eps = _first_seq(first, [*rhs[d + 1 :], la])
            for q, (lh, _rh) in enumerate(prods):
                if lh != b:
                    continue
                for x in fset:
                    key = (q, 0, x)
                    if key not in out:
                        out[key] = True
                        work.append(key)
    return out


def _goto(prods, items, first, sym):
    moved = {}
    for p, d, la in items:
        _lhs, rhs = prods[p]
        if d < len(rhs) and rhs[d] == sym:
            moved[(p, d + 1, la)] = True
    if not moved:
        return None
    return _closure(prods, moved, first)


def _build(prods, first, terms, nonterms):
    aug = [("$S", [prods[0][0]]), *prods]
    first = dict(first)
    first["$S"] = {prods[0][0]}
    start = _closure(aug, {(0, 0, "$"): True}, first)
    states = [start]
    index = {frozenset(start): 0}
    trans = {}
    queue = [0]
    while queue:
        si = queue.pop(0)
        for x in terms + nonterms:
            g = _goto(aug, states[si], first, x)
            if g is None:
                continue
            key = frozenset(g)
            if key not in index:
                index[key] = len(states)
                states.append(g)
                queue.append(len(states) - 1)
            trans[(si, x)] = index[key]
    return aug, states, trans


def _merge(states):
    cores = []
    for st in states:
        core = frozenset((p, d) for p, d, _ in st)
        if core not in cores:
            cores.append(core)
    cls_of = [cores.index(frozenset((p, d) for p, d, _ in st)) for st in states]
    members_of = [[] for _ in cores]
    for si, ci in enumerate(cls_of):
        members_of[ci].append(si)
    return members_of, cls_of


def _cell(action, key, ent):
    if key in action and action[key] != ent:
        action[key] = ent
        return True
    action[key] = ent
    return False


def _action_for(aug, terms, look, members, trans, cls_of, ci, action):
    conflict = False
    for (p, d), las in look.items():
        _lhs, rhs = aug[p]
        if d < len(rhs) and rhs[d] in terms:
            tgt = None
            for si in members:
                if (si, rhs[d]) in trans:
                    tgt = cls_of[trans[(si, rhs[d])]]
                    break
            conflict |= _cell(action, (ci, rhs[d]), ("s", tgt))
        elif d == len(rhs) and p > 0:
            for la in las:
                conflict |= _cell(action, (ci, la), ("r", p))
        elif d == len(rhs) and p == 0:
            conflict |= _cell(action, (ci, "$"), ("acc", 0))
    return conflict


def _tables(aug, states, trans, terms, nonterms):
    members_of, cls_of = _merge(states)
    action, goto = {}, {}
    conflict = False
    for ci, members in enumerate(members_of):
        look = {}
        for si in members:
            for p, d, la in states[si]:
                look.setdefault((p, d), set()).add(la)
        conflict |= _action_for(aug, terms, look, members, trans, cls_of, ci, action)
        for (p, d), _las in look.items():
            _lhs, rhs = aug[p]
            if d < len(rhs) and rhs[d] in nonterms:
                for si in members:
                    if (si, rhs[d]) in trans:
                        goto[(ci, rhs[d])] = cls_of[trans[(si, rhs[d])]]
                        break
    return action, goto, len(members_of), conflict, cls_of[0]


def _parse(action, goto, start_key, toks, aug):
    stack = [start_key]
    toks = [*toks, "$"]
    pos, reds = 0, []
    while True:
        ent = action.get((stack[-1], toks[pos]))
        if ent is None:
            return None
        if ent[0] == "s":
            stack.append(ent[1])
            pos += 1
        elif ent[0] == "r":
            _lhs, rhs = aug[ent[1]]
            if rhs:
                del stack[-len(rhs) :]
            g = goto.get((stack[-1], _lhs))
            if g is None:
                return None
            stack.append(g)
            reds.append(ent[1])
        else:
            return reds


def _run(prods, queries):
    nonterms = []
    for lhs, _ in prods:
        if lhs not in nonterms:
            nonterms.append(lhs)
    terms = []
    for _, rhs in prods:
        for s in rhs:
            if s not in nonterms and s not in terms:
                terms.append(s)
    first = _first_sets(prods)
    aug, states, trans = _build(prods, first, terms, nonterms)
    action, goto, ncls, conflict, start = _tables(aug, states, trans, terms, nonterms)
    if conflict:
        return ["CONFLICT"]
    out = [f"STATES {ncls}"]
    for toks in queries:
        reds = _parse(action, goto, start, toks, aug)
        if reds is None:
            out.append("REJECT")
        elif reds:
            out.append("ACCEPT " + " ".join(map(str, reds)))
        else:
            out.append("ACCEPT")
    return out


def main():
    data = sys.stdin.read().split("\n")
    if not data or not data[0].strip():
        return
    m = int(data[0].split()[0])
    prods = []
    for i in range(1, 1 + m):
        parts = data[i].split()
        prods.append((parts[0], parts[2:]))
    q = int(data[1 + m].split()[0])
    queries = [data[2 + m + i].split() for i in range(q)]
    sys.stdout.write("\n".join(_run(prods, queries)))


if __name__ == "__main__":
    main()
