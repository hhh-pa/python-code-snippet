"""ABD multi-writer atomic register emulation (Lynch 17.1.3 + MWMR)."""

import sys


def _run(n, crashed, ops):
    correct = [p for p in range(n) if p not in crashed]
    quorum = n // 2 + 1
    val = [0] * n
    seq = [0] * n
    wid = [0] * n
    out = []
    for op in ops:
        if len(correct) < quorum or op[1] in crashed:
            out.append("BLOCKED")
            continue
        if op[0] == "W":
            _, p, v = op
            s = max(seq[r] for r in correct)
            ns = s + 1
            for r in correct:
                if (ns, p) > (seq[r], wid[r]):
                    val[r], seq[r], wid[r] = v, ns, p
            out.append(f"ACK {ns} {p}")
        else:
            best = max((seq[r], wid[r], val[r]) for r in correct)
            s, w, v = best
            for r in correct:
                if (s, w) > (seq[r], wid[r]):
                    val[r], seq[r], wid[r] = v, s, w
            out.append(f"VAL {v} {s} {w}")
    return out


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n, m = int(toks[0]), int(toks[1])
    k = int(toks[2])
    crashed = set(map(int, toks[3 : 3 + k]))
    ops = []
    i = 3 + k
    for _ in range(m):
        if toks[i] == "W":
            ops.append(("W", int(toks[i + 1]), int(toks[i + 2])))
            i += 3
        else:
            ops.append(("R", int(toks[i + 1])))
            i += 2
    sys.stdout.write("\n".join(_run(n, crashed, ops)))


if __name__ == "__main__":
    main()
