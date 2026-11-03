import sys

def is_terminal(c):
    return not ('A' <= c <= 'Z') and c != '#'

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    idx = 0
    try:
        num_prods = int(tokens[idx])
    except (ValueError, IndexError):
        return
    idx += 1
    if idx >= len(tokens):
        return
    start_symbol = tokens[idx][0]
    idx += 1

    prods = []
    non_terminals = set()
    terminals = {'$'}

    for _ in range(num_prods):
        if idx >= len(tokens):
            return
        lhs = tokens[idx][0]
        # arrow
        rhs = tokens[idx + 2]
        idx += 3
        prods.append((lhs, rhs))
        non_terminals.add(lhs)
        for c in rhs:
            if is_terminal(c):
                terminals.add(c)
            elif c != '#':
                non_terminals.add(c)

    # Step 1: FIRST sets
    first = {t: {t} for t in terminals}
    for nt in non_terminals:
        first[nt] = set()

    changed = True
    while changed:
        changed = False
        for A, rhs in prods:
            old_size = len(first[A])
            if rhs == "#":
                first[A].add('#')
            else:
                all_eps = True
                for sym in rhs:
                    sym_has_eps = False
                    for f in first[sym]:
                        if f == '#':
                            sym_has_eps = True
                        else:
                            first[A].add(f)
                    if not sym_has_eps:
                        all_eps = False
                        break
                if all_eps:
                    first[A].add('#')
            if len(first[A]) > old_size:
                changed = True

    def first_of_string(s):
        res = set()
        if s == "#" or not s:
            res.add('#')
            return res
        all_eps = True
        for sym in s:
            sym_has_eps = False
            for f in first.get(sym, set()):
                if f == '#':
                    sym_has_eps = True
                else:
                    res.add(f)
            if not sym_has_eps:
                all_eps = False
                break
        if all_eps:
            res.add('#')
        return res

    # Step 2: FOLLOW sets
    follow = {nt: set() for nt in non_terminals}
    follow[start_symbol].add('$')

    changed = True
    while changed:
        changed = False
        for A, rhs in prods:
            if rhs == "#":
                continue
            for i in range(len(rhs)):
                B = rhs[i]
                if is_terminal(B):
                    continue
                old_size = len(follow[B])
                rest = rhs[i + 1:]
                first_rest = first_of_string(rest)
                for f in first_rest:
                    if f != '#':
                        follow[B].add(f)
                if '#' in first_rest:
                    for fol in follow[A]:
                        follow[B].add(fol)
                if len(follow[B]) > old_size:
                    changed = True

    # Step 3: LL(1) Table construction
    table = {}
    is_ll1 = True

    for p_idx, (A, rhs) in enumerate(prods):
        f_rhs = first_of_string(rhs)
        for a in f_rhs:
            if a != '#':
                key = (A, a)
                if key in table and table[key] != p_idx:
                    is_ll1 = False
                table[key] = p_idx
        if '#' in f_rhs:
            for b in follow[A]:
                key = (A, b)
                if key in table and table[key] != p_idx:
                    is_ll1 = False
                table[key] = p_idx

    out = []
    if not is_ll1:
        out.append("GRAMMAR IS NOT LL1")
        sys.stdout.write("\n".join(out) + "\n")
        return

    out.append("GRAMMAR IS LL1")

    if idx < len(tokens):
        num_queries = int(tokens[idx])
        idx += 1
        for _ in range(num_queries):
            if idx >= len(tokens):
                break
            w = tokens[idx] + '$'
            idx += 1

            stack = ['$', start_symbol]
            ip = 0
            derivations = []
            ok = True

            while stack:
                X = stack.pop()
                a = w[ip] if ip < len(w) else '$'

                if X == a:
                    ip += 1
                    if X == '$':
                        break
                elif is_terminal(X):
                    ok = False
                    break
                else:
                    key = (X, a)
                    if key not in table:
                        ok = False
                        break
                    rule_idx = table[key]
                    derivations.append(rule_idx)
                    rhs = prods[rule_idx][1]
                    if rhs != "#":
                        for k in range(len(rhs) - 1, -1, -1):
                            stack.append(rhs[k])

            if ok and ip == len(w):
                out.append(" ".join(f"r{d}" for d in derivations))
            else:
                out.append("SYNTAX ERROR")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
