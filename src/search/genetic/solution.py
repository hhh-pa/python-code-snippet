"""Genetic algorithms for N-queens (AIMA 4.1.4)."""

import sys

MOD = 1 << 31


def _fitness(s):
    n = len(s)
    bad = 0
    for i in range(n):
        for j in range(i + 1, n):
            if s[i] == s[j] or abs(i - j) == abs(s[i] - s[j]):
                bad += 1
    return n * (n - 1) // 2 - bad


def _run(n, pop, gens, mnum, mden, seed):
    rng = seed

    def draw(upper):
        nonlocal rng
        rng = (1103515245 * rng + 12345) % MOD
        return rng % upper

    def select(fit, total):
        if total == 0:
            return list(pop[draw(len(pop))])
        w = draw(total)
        acc = 0
        for s, f in zip(pop, fit):
            acc += f
            if w < acc:
                return list(s)
        return list(pop[-1])

    for _ in range(gens):
        fit = [_fitness(s) for s in pop]
        total = sum(fit)
        nxt = []
        for _ in range(len(pop) // 2):
            a, b = select(fit, total), select(fit, total)
            c = 1 + draw(n - 1)
            for child in (a[:c] + b[c:], b[:c] + a[c:]):
                mut = [(1 + draw(n)) if draw(mden) < mnum else g for g in child]
                nxt.append(mut)
        pop = nxt
    return pop


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    n, p, g, mnum, mden, seed = (
        int(toks[0]),
        int(toks[1]),
        int(toks[2]),
        int(toks[3]),
        int(toks[4]),
        int(toks[5]),
    )
    pop = [list(map(int, toks[6 + i])) for i in range(p)]
    pop = _run(n, pop, g, mnum, mden, seed)
    out = ["".join(map(str, s)) for s in pop]
    fit = [_fitness(s) for s in pop]
    bi = max(range(len(pop)), key=lambda i: fit[i])
    out.append(f"BEST {''.join(map(str, pop[bi]))} {fit[bi]}")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
