import sys
import heapq

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    v = int(next(it))
    e = int(next(it))

    graph = [[] for _ in range(v)]
    indegree = [0] * v

    for _ in range(e):
        frm = int(next(it))
        to = int(next(it))
        graph[frm].append(to)
        indegree[to] += 1

    q = [-i for i in range(v) if indegree[i] == 0]
    heapq.heapify(q)

    ans = []
    while q:
        node = -heapq.heappop(q)
        ans.append(node)
        for w in graph[node]:
            indegree[w] -= 1
            if indegree[w] == 0:
                heapq.heappush(q, -w)

    print(" ".join(str(x) for x in ans))

if __name__ == "__main__":
    main()
