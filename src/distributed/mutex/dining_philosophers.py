import sys

MASK64 = 0xFFFFFFFFFFFFFFFF

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        R = int(next(it))
    except StopIteration:
        return

    lcg_state = 12345

    def lcg_next():
        nonlocal lcg_state
        lcg_state = (lcg_state * 6364136223846793005 + 1442695040888963407) & MASK64
        return lcg_state

    fork = [0] * n
    hungry = [0] * n
    held = [-1] * n
    eatst = [0] * n
    eats = [0] * n
    waits = [0] * n

    for _ in range(R):
        for i in range(n):
            if not hungry[i] and not eatst[i] and ((lcg_next() >> 16) % 100 < 60):
                hungry[i] = 1
                held[i] = -1

        for i in range(n):
            if not hungry[i] or held[i] != -1:
                continue
            f1 = i if ((lcg_next() >> 33) % 2 == 0) else (i + 1) % n
            if fork[f1] == 0:
                fork[f1] = i + 1
                held[i] = f1

        for i in range(n):
            if not hungry[i] or held[i] == -1 or eatst[i]:
                continue
            lf = i
            rt = (i + 1) % n
            f2 = rt if held[i] == lf else lf
            if fork[f2] == 0:
                fork[f2] = i + 1
                eatst[i] = 1
            else:
                fork[held[i]] = 0
                held[i] = -1

        for i in range(n):
            if eatst[i] == 2:
                fork[i] = 0
                fork[(i + 1) % n] = 0
                eatst[i] = 0
                hungry[i] = 0
                eats[i] += 1
            elif eatst[i] == 1:
                eatst[i] = 2
            elif hungry[i]:
                waits[i] += 1

    tot = sum(eats)
    stuck = sum(1 for x in fork if x != 0)

    out = []
    for i in range(n):
        out.append(f"P{i}: eats={eats[i]} waits={waits[i]}")
    out.append(f"TOTALEATS: {tot}")
    out.append(f"STUCK: {stuck}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
