import sys

MASK64 = 0xFFFFFFFFFFFFFFFF

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n = int(next(it))
        f = int(next(it))
        rmax = int(next(it))
    except StopIteration:
        return

    x = [int(next(it)) for _ in range(n)]
    k = int(next(it))
    faulty = [0] * n
    for _ in range(k):
        faulty[int(next(it))] = 1

    lcg = 777
    def flip():
        nonlocal lcg
        lcg = (lcg * 6364136223846793005 + 1442695040888963407) & MASK64
        return (lcg >> 33) % 2

    nc = sum(1 for v in faulty if not v)
    decision = -1
    rounds = 0
    flips = 0

    for r in range(1, rmax + 1):
        rounds = r
        o = 0
        z = 0
        for i in range(n):
            if not faulty[i]:
                if x[i] == 1:
                    o += 1
                else:
                    z += 1
        prop = -1
        if o > n // 2:
            prop = 1
        elif z > n // 2:
            prop = 0

        if prop >= 0:
            if nc >= f + 1:
                decision = prop
                break
            for i in range(n):
                if not faulty[i]:
                    x[i] = prop
        else:
            for i in range(n):
                if not faulty[i]:
                    x[i] = flip()
                    flips += 1

    out = []
    if decision >= 0:
        out.append(f"DECISION: {decision}")
    else:
        out.append("DECISION: UNDECIDED")
    out.append(f"ROUNDS: {rounds}")
    out.append(f"COINFLIPS: {flips}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
