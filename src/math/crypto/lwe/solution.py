import sys


def main():
    toks = sys.stdin.read().split()
    if len(toks) < 5:
        return
    if toks[0] == "ENC":
        n, q, mu = (int(t) for t in toks[1:4])
        rest = [int(t) for t in toks[4:]]
        m = len(rest) // (n + 2)
        a = [rest[i * n : (i + 1) * n] for i in range(m)]
        b = rest[m * n : m * n + m]
        r = rest[m * n + m :]
        u = [sum(r[i] * a[i][j] for i in range(m)) % q for j in range(n)]
        v = (sum(r[i] * b[i] for i in range(m)) + mu * (q // 2)) % q
        sys.stdout.write(" ".join(map(str, u)) + f" {v}")
    else:
        n, q = int(toks[1]), int(toks[2])
        rest = [int(t) for t in toks[3:]]
        s, u, v = rest[:n], rest[n : 2 * n], rest[2 * n]
        x = (v - sum(a * b for a, b in zip(s, u))) % q
        sys.stdout.write("0" if min(x, q - x) < q / 4 else "1")


if __name__ == "__main__":
    main()
