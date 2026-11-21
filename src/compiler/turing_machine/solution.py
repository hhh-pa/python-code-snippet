"""Bounded-step deterministic Turing machine simulation (Rosen 13)."""

import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    pos = 0
    _nstates, accept, reject, bound = (int(toks[pos + i]) for i in range(4))
    pos += 4
    m = int(toks[pos])
    pos += 1
    trans = {}
    for _ in range(m):
        q, a, b = toks[pos], toks[pos + 1], toks[pos + 2]
        d, q2 = toks[pos + 3], toks[pos + 4]
        pos += 5
        trans[(int(q), a)] = (b, d, int(q2))
    word = toks[pos] if pos < len(toks) else ""
    tape = {}
    for i, ch in enumerate(word):
        tape[i] = ch
    state, head, steps = 0, 0, 0
    while steps < bound:
        sym = tape.get(head, ".")
        key = (state, sym)
        if key not in trans:
            sys.stdout.write(f"REJECT {steps}")
            return
        write, move, state = trans[key]
        tape[head] = write
        head += {"L": -1, "R": 1, "S": 0}[move]
        steps += 1
        if state == accept:
            sys.stdout.write(f"ACCEPT {steps}")
            return
        if state == reject:
            sys.stdout.write(f"REJECT {steps}")
            return
    sys.stdout.write("TIMEOUT")


if __name__ == "__main__":
    main()
