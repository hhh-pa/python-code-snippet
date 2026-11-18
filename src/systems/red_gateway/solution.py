"""RED gateway simulation (Tanenbaum 5.4 + Floyd-Jacobson 1993)."""

import sys

SCALE = 1000
MOD = 1 << 31


def _run(wqn, wqd, mn, mx, pn, pd, cap, seed, arrivals):
    q = 0
    avg = 0
    count = 0
    rng = seed
    now = 0
    out = []
    for t in arrivals:
        while now <= t:
            if q > 0:
                q -= 1
            else:
                avg = avg * (wqd - wqn) // wqd
            now += 1
        avg = (avg * (wqd - wqn) + wqn * q * SCALE) // wqd
        if q == cap:
            out.append("DROP")
            count = 0
        elif avg < mn * SCALE:
            out.append("ENQUEUE")
            q += 1
            count = 0
        elif avg >= mx * SCALE:
            out.append("DROP")
            count = 0
        else:
            count += 1
            a = avg - mn * SCALE
            r = (mx - mn) * SCALE
            if count * pn * a >= pd * r:
                out.append("DROP")
                count = 0
            else:
                rng = (1103515245 * rng + 12345) % MOD
                if rng * (pd * r - count * pn * a) < MOD * pn * a:
                    out.append("DROP")
                    count = 0
                else:
                    out.append("ENQUEUE")
                    q += 1
    out.append(f"FINAL {q} {avg} {count}")
    return out


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    p = list(map(int, toks[:8]))
    m = int(toks[8])
    arrivals = list(map(int, toks[9 : 9 + m]))
    sys.stdout.write("\n".join(_run(*p, arrivals)))


if __name__ == "__main__":
    main()
