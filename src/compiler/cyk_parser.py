import sys

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
    start_symbol = ord(tokens[idx][0])
    idx += 1

    term_rules = []
    nonterm_rules = []

    for _ in range(num_rules):
        if idx >= len(tokens):
            return
        lhs = ord(tokens[idx][0])
        idx += 1
        if idx >= len(tokens):
            return
        idx += 1  # arrow
        if idx >= len(tokens):
            return
        rhs = tokens[idx]
        idx += 1
        if len(rhs) == 1:
            term_rules.append((lhs, ord(rhs[0])))
        elif len(rhs) == 2:
            nonterm_rules.append((lhs, ord(rhs[0]), ord(rhs[1])))

    if idx >= len(tokens):
        return

    try:
        num_queries = int(tokens[idx])
    except (ValueError, IndexError):
        return
    idx += 1

    MOD = 1000000007
    out = []

    for _ in range(num_queries):
        if idx >= len(tokens):
            break
        w = tokens[idx]
        idx += 1
        n = len(w)
        if n == 0:
            out.append("NO 0")
            continue

        w_ords = [ord(c) for c in w]

        # dp[length][start] -> dict: symbol -> count
        dp = [[{} for _ in range(n)] for _ in range(n + 1)]

        for i in range(n):
            ch = w_ords[i]
            dp_1_i = dp[1][i]
            for lhs, term in term_rules:
                if term == ch:
                    dp_1_i[lhs] = (dp_1_i.get(lhs, 0) + 1) % MOD

        for length in range(2, n + 1):
            for i in range(n - length + 1):
                dp_len_i = dp[length][i]
                for k in range(1, length):
                    left_dp = dp[k][i]
                    if not left_dp:
                        continue
                    right_dp = dp[length - k][i + k]
                    if not right_dp:
                        continue
                    for lhs, r1, r2 in nonterm_rules:
                        w1 = left_dp.get(r1, 0)
                        if not w1:
                            continue
                        w2 = right_dp.get(r2, 0)
                        if not w2:
                            continue
                        add = (w1 * w2) % MOD
                        dp_len_i[lhs] = (dp_len_i.get(lhs, 0) + add) % MOD

        ways = dp[n][0].get(start_symbol, 0)
        if ways > 0:
            out.append(f"YES {ways}")
        else:
            out.append("NO 0")

    if out:
        sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
