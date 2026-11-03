import sys

sys.setrecursionlimit(200000)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    N = 2 * n
    adj = [[] for _ in range(N)]

    def lit(k):
        v = abs(k) - 1
        return 2 * v + 1 if k > 0 else 2 * v

    for _ in range(m):
        a = int(next(it))
        b = int(next(it))
        adj[lit(-a)].append(lit(b))
        adj[lit(-b)].append(lit(a))

    idx = [0] * N
    low = [0] * N
    on = [False] * N
    comp = [-1] * N
    st = []
    C = 0
    T = 0

    def dfs(v):
        nonlocal C, T
        T += 1
        idx[v] = low[v] = T
        st.append(v)
        on[v] = True

        for w in adj[v]:
            if idx[w] == 0:
                dfs(w)
                if low[w] < low[v]:
                    low[v] = low[w]
            elif on[w]:
                if idx[w] < low[v]:
                    low[v] = idx[w]

        if low[v] == idx[v]:
            while True:
                x = st.pop()
                on[x] = False
                comp[x] = C
                if x == v:
                    break
            C += 1

    for v in range(N):
        if idx[v] == 0:
            dfs(v)

    for i in range(n):
        if comp[2 * i] == comp[2 * i + 1]:
            print("UNSATISFIABLE")
            return

    print("SATISFIABLE")
    ans = [("1" if comp[2 * i] > comp[2 * i + 1] else "0") for i in range(n)]
    print(" ".join(ans))

if __name__ == "__main__":
    main()
