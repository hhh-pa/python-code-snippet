import sys
from collections import deque

class Edge:
    __slots__ = ('to', 'rev', 'cap', 'flow')
    def __init__(self, to, rev, cap, flow=0):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.flow = flow

class Dinic:
    def __init__(self, n, s, t):
        self.n = n
        self.s = s
        self.t = t
        self.adj = [[] for _ in range(n)]
        self.level = [-1] * n
        self.ptr = [0] * n

    def add_edge(self, from_node, to_node, cap):
        self.adj[from_node].append(Edge(to_node, len(self.adj[to_node]), cap, 0))
        self.adj[to_node].append(Edge(from_node, len(self.adj[from_node]) - 1, 0, 0))

    def bfs(self):
        self.level = [-1] * self.n
        self.level[self.s] = 0
        q = deque([self.s])
        while q:
            v = q.popleft()
            for edge in self.adj[v]:
                if edge.cap - edge.flow > 0 and self.level[edge.to] == -1:
                    self.level[edge.to] = self.level[v] + 1
                    q.append(edge.to)
        return self.level[self.t] != -1

    def dfs(self, v, pushed):
        if pushed == 0 or v == self.t:
            return pushed
        adj_v = self.adj[v]
        for cid in range(self.ptr[v], len(adj_v)):
            self.ptr[v] = cid
            edge = adj_v[cid]
            tr = edge.to
            if self.level[v] + 1 != self.level[tr] or edge.cap - edge.flow <= 0:
                continue
            tr_pushed = self.dfs(tr, min(pushed, edge.cap - edge.flow))
            if tr_pushed == 0:
                continue
            edge.flow += tr_pushed
            self.adj[tr][edge.rev].flow -= tr_pushed
            return tr_pushed
        self.ptr[v] = len(adj_v)
        return 0

    def max_flow(self):
        flow = 0
        INF = 10**18
        while self.bfs():
            self.ptr = [0] * self.n
            while True:
                pushed = self.dfs(self.s, INF)
                if pushed == 0:
                    break
                flow += pushed
        return flow

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    s = int(next(it))
    t = int(next(it))

    dinic = Dinic(n, s, t)
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        cap = int(next(it))
        dinic.add_edge(u, v, cap)

    print(dinic.max_flow())

if __name__ == "__main__":
    main()
