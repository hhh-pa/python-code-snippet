import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    M = int(tokens[1])
    words = tokens[2 : 2 + n]
    length = [len(w) for w in words]

    INF = 10**18
    cost = [INF] * (n + 1)
    cost[n] = 0

    for i in range(n - 1, -1, -1):
        ll = 0
        best = INF
        for j in range(i, n):
            ll += length[j] + (1 if j > i else 0)
            if ll > M:
                break
            c = 0 if j == n - 1 else (M - ll) ** 3
            val = c + cost[j + 1]
            if val < best:
                best = val
        cost[i] = best

    print(cost[0])

if __name__ == '__main__':
    main()
