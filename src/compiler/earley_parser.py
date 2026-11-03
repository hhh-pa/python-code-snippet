import sys

def is_terminal_symbol(c):
    return not ('A' <= c <= 'Z') and c != '#'

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    idx = 0
    try:
        num_rules = int(tokens[idx])
    except (ValueError, IndexError):
        return
    idx += 1
    if idx >= len(tokens):
        return
    start_symbol = tokens[idx][0]
    idx += 1

    prods = [('@', start_symbol)]
    for _ in range(num_rules):
        if idx >= len(tokens):
            return
        lhs = tokens[idx][0]
        idx += 1
        if idx >= len(tokens):
            return
        idx += 1  # arrow
        if idx >= len(tokens):
            return
        rhs = tokens[idx]
        idx += 1
        if rhs == "#":
            rhs = ""
        prods.append((lhs, rhs))

    if idx >= len(tokens):
        return
    try:
        num_queries = int(tokens[idx])
    except (ValueError, IndexError):
        return
    idx += 1

    out = []
    for _ in range(num_queries):
        if idx >= len(tokens):
            break
        w = tokens[idx]
        idx += 1
        if w == "EPS":
            w = ""
        n = len(w)

        chart = [[] for _ in range(n + 1)]
        in_chart = [set() for _ in range(n + 1)]

        def add_item(k, item):
            if item not in in_chart[k]:
                in_chart[k].add(item)
                chart[k].append(item)

        add_item(0, (0, 0, 0))
        total_items = 0

        for k in range(n + 1):
            i = 0
            while i < len(chart[k]):
                rule_id, dot, origin = chart[k][i]
                i += 1
                lhs, rhs = prods[rule_id]
                if dot < len(rhs):
                    next_sym = rhs[dot]
                    if not is_terminal_symbol(next_sym):
                        # Predictor
                        for r in range(len(prods)):
                            if prods[r][0] == next_sym:
                                add_item(k, (r, 0, k))
                    else:
                        # Scanner
                        if k < n and w[k] == next_sym:
                            add_item(k + 1, (rule_id, dot + 1, origin))
                else:
                    # Completer
                    completed_lhs = lhs
                    origin_items = chart[origin]
                    for j in range(len(origin_items)):
                        prev_rule_id, prev_dot, prev_origin = origin_items[j]
                        prev_rhs = prods[prev_rule_id][1]
                        if prev_dot < len(prev_rhs) and prev_rhs[prev_dot] == completed_lhs:
                            add_item(k, (prev_rule_id, prev_dot + 1, prev_origin))
            total_items += len(chart[k])

        accepted = (0, 1, 0) in in_chart[n]
        if accepted:
            out.append(f"ACCEPT {total_items}")
        else:
            out.append(f"REJECT {total_items}")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
