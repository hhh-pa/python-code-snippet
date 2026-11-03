import sys
from collections import deque

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))

    mp = [[0] * n for _ in range(n)]
    wp = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mp[i][j] = int(next(it))
    for i in range(n):
        for j in range(n):
            wp[i][j] = int(next(it))

    rank = [[0] * n for _ in range(n)]
    for w in range(n):
        for r in range(n):
            rank[w][wp[w][r]] = r

    wife = [-1] * n
    husb = [-1] * n
    nxt = [0] * n
    free_men = deque(range(n))

    while free_men:
        m = free_men.popleft()
        w = mp[m][nxt[m]]
        nxt[m] += 1
        curr_h = husb[w]
        if curr_h == -1:
            wife[m] = w
            husb[w] = m
        elif rank[w][m] < rank[w][curr_h]:
            wife[curr_h] = -1
            free_men.append(curr_h)
            wife[m] = w
            husb[w] = m
        else:
            free_men.append(m)

    out = []
    for m in range(n):
        out.append(f"{m} {wife[m]}")
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
