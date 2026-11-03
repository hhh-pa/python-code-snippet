import sys

MOD = 1000000007

def mod_norm(x):
    r = x % MOD
    return r if r >= 0 else r + MOD

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n < 0:
        return
    idx = 1
    c = [mod_norm(int(tokens[idx + i])) for i in range(n + 1)]
    idx += n + 1
    q = int(tokens[idx])
    idx += 1

    out = []
    for _ in range(q):
        x = mod_norm(int(tokens[idx]))
        idx += 1
        res = c[n]
        for i in range(n - 1, -1, -1):
            res = (res * x + c[i]) % MOD
        out.append(str(res))
    print(" ".join(out))

if __name__ == '__main__':
    main()
