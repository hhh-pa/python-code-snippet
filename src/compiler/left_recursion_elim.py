import sys

def syms_of(s):
    r = []
    i = 0
    n = len(s)
    while i < n:
        if 'A' <= s[i] <= 'Z':
            t = [s[i]]
            i += 1
            while i < n and s[i] == "'":
                t.append(s[i])
                i += 1
            r.append("".join(t))
        else:
            r.append(s[i])
            i += 1
    return r

def show_alt(a):
    if not a:
        return "@"
    return "".join(a)

def fresh_for(base, rules):
    b = base
    while True:
        b += "'"
        if not any(rl[0] == b for rl in rules):
            return b

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    idx = 0
    try:
        T = int(tokens[idx])
    except (ValueError, IndexError):
        return
    idx += 1

    out = []
    for _ in range(T):
        if idx >= len(tokens):
            break
        R = int(tokens[idx])
        idx += 1

        rules = []
        for _ in range(R):
            line = tokens[idx]
            idx += 1
            eq = line.find('=')
            lhs = line[:eq]
            alts_str = line[eq + 1:]
            alts = []
            for a in alts_str.split('|'):
                if a == "@" or not a:
                    alts.append([])
                else:
                    alts.append(syms_of(a))
            rules.append([lhs, alts])

        n0 = len(rules)
        for i in range(n0):
            for j in range(i):
                na = []
                for a in rules[i][1]:
                    if a and a[0] == rules[j][0]:
                        for b in rules[j][1]:
                            na.append(b + a[1:])
                    else:
                        na.append(a)
                rules[i][1] = na

            # dedup
            dd = []
            for a in rules[i][1]:
                if a not in dd:
                    dd.append(a)
            rules[i][1] = dd

            # immediate elimination
            rec = []
            nonrec = []
            for a in rules[i][1]:
                if a and a[0] == rules[i][0]:
                    rec.append(a[1:])
                else:
                    nonrec.append(a)

            if rec:
                np = fresh_for(rules[i][0], rules)
                if not nonrec:
                    nalts = [[np]]
                else:
                    nalts = [b + [np] for b in nonrec]
                rules[i][1] = nalts
                palts = [d + [np] for d in rec]
                if nonrec:
                    palts.append([])
                rules.append([np, palts])

        # left factoring to fixed point
        for _ in range(20):
            any_factored = False
            for i in range(len(rules)):
                groups = {}
                for k, alt in enumerate(rules[i][1]):
                    key = "" if not alt else alt[0]
                    groups.setdefault(key, []).append(k)

                # Iterate in sorted order of key like C++ std::map
                for key in sorted(groups.keys()):
                    indices = groups[key]
                    if len(indices) < 2:
                        continue
                    g = [rules[i][1][k] for k in indices]
                    pre = 0
                    while True:
                        ok = True
                        for k in range(1, len(g)):
                            if pre >= len(g[k]) or pre >= len(g[0]) or g[k][pre] != g[0][pre]:
                                ok = False
                                break
                        if not ok or pre >= len(g[0]):
                            break
                        pre += 1
                    if pre == 0:
                        continue
                    np = fresh_for(rules[i][0], rules)
                    prefix = g[0][:pre]
                    first_new = prefix + [np]
                    keep = []
                    suflist = []
                    in_g = set(indices)
                    placed = False
                    for k, alt in enumerate(rules[i][1]):
                        if k in in_g:
                            if not placed:
                                keep.append(first_new)
                                placed = True
                            suflist.append(alt[pre:])
                        else:
                            keep.append(alt)
                    rules[i][1] = keep
                    rules.append([np, suflist])
                    any_factored = True
                    break
                if any_factored:
                    break
            if not any_factored:
                break

        out.append(f"GRAMMAR {len(rules)}")
        for lhs, alts in rules:
            alt_strs = [show_alt(a) for a in alts]
            out.append(f"{lhs}={'|'.join(alt_strs)}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
