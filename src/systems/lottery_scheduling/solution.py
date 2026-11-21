"""Lottery scheduling (MOS 2.4, Waldspurger-Weihl)."""

import sys

MOD = 1 << 31


def _run(n, seed, events):
    tickets = [0] * n
    total = 0
    rng = seed
    out = []
    for ev in events:
        if ev[0] == "DRAW":
            if total == 0:
                out.append("EMPTY")
                continue
            limit = (MOD // total) * total
            while True:
                rng = (1103515245 * rng + 12345) % MOD
                if rng < limit:
                    break
            w = rng % total
            acc, win = 0, 0
            for p, t in enumerate(tickets):
                acc += t
                if w < acc:
                    win = p
                    break
            out.append(f"WINNER {win}")
        elif ev[0] == "SET":
            _, p, t = ev
            total += t - tickets[p]
            tickets[p] = t
            out.append(f"OK {total}")
        else:
            _, a, b, t = ev
            if tickets[a] < t:
                out.append("REJECTED")
            else:
                tickets[a] -= t
                tickets[b] += t
                out.append(f"OK {total}")
    return out


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n, e, seed = int(toks[0]), int(toks[1]), int(toks[2])
    events = []
    i = 3
    for _ in range(e):
        if toks[i] == "DRAW":
            events.append(("DRAW",))
            i += 1
        elif toks[i] == "SET":
            events.append(("SET", int(toks[i + 1]), int(toks[i + 2])))
            i += 3
        else:
            events.append(
                ("XFER", int(toks[i + 1]), int(toks[i + 2]), int(toks[i + 3]))
            )
            i += 4
    sys.stdout.write("\n".join(_run(n, seed, events)))


if __name__ == "__main__":
    main()
