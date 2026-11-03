import sys
from collections import deque

class Edge:
    __slots__ = ('to', 'rev', 'cap', 'flow')
    def __init__(self, to, rev, cap, flow=0):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.flow = flow

class PushRelabel:
    def __init__(self, n, s, t):
        self.n = n
        self.s = s
        self.t = t
        self.adj = [[] for _ in range(n)]
        self.excess = [0] * n
        self.height = [0] * n
        self.count = [0] * (2 * n)
        self.in_queue = [False] * n
        self.active_q = deque()

    def add_edge(self, from_node, to_node, cap):
        self.adj[from_node].append(Edge(to_node, len(self.adj[to_node]), cap, 0))
        self.adj[to_node].append(Edge(from_node, len(self.adj[from_node]) - 1, 0, 0))

    def enqueue(self, u):
        if not self.in_queue[u] and u != self.s and u != self.t and self.excess[u] > 0:
            self.in_queue[u] = True
            self.active_q.append(u)

    def push(self, u, edge):
        amt = min(self.excess[u], edge.cap - edge.flow)
        if amt == 0 or self.height[u] != self.height[edge.to] + 1:
            return
        edge.flow += amt
        self.adj[edge.to][edge.rev].flow -= amt
        self.excess[u] -= amt
        self.excess[edge.to] += amt
        self.enqueue(edge.to)

    def relabel(self, u):
        min_h = 2 * self.n
        for edge in self.adj[u]:
            if edge.cap - edge.flow > 0:
                if edge_h := self.height[edge.to]:
                    if edge_h < min_h:
                        min_h = edge_h
                else:
                    min_h = 0
        if min_h < 2 * self.n:
            old_h = self.height[u]
            self.count[old_h] -= 1
            self.height[u] = min_h + 1
            self.count[self.height[u]] += 1

    def discharge(self, u):
        idx = 0
        adj_u = self.adj[u]
        len_adj = len(adj_u)
        while self.excess[u] > 0:
            if idx < len_adj:
                edge = adj_u[idx]
                if edge.cap - edge.flow > 0 and self.height[u] == self.height[edge.to] + 1:
                    self.push(u, edge)
                else:
                    idx += 1
            else:
                self.relabel(u)
                idx = 0

    def max_flow(self):
        self.height[self.s] = self.n
        self.count[self.n] = 1
        self.count[0] = self.n - 1

        for edge in self.adj[self.s]:
            amt = edge.cap
            if amt > 0:
                edge.flow += amt
                self.adj[edge.to][edge.rev].flow -= amt
                self.excess[edge.to] += amt
                self.excess[self.s] -= amt
                self.enqueue(edge.to)

        while self.active_q:
            u = self.active_q.popleft()
            self.in_queue[u] = False
            self.discharge(u)

        return self.excess[self.t]

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))
    s = int(next(it))
    t = int(next(it))

    pr = PushRelabel(n, s, t)
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        cap = int(next(it))
        pr.add_edge(u, v, cap)

    print(pr.max_flow())

if __name__ == "__main__":
    main()
