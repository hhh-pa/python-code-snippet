import sys
import heapq

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    if mode == "E":
        n = int(tokens[1])
        adj = [set() for _ in range(n)]
        deg = [0] * n
        idx = 2
        for _ in range(n - 1):
            u = int(tokens[idx])
            v = int(tokens[idx+1])
            idx += 2
            adj[u].add(v)
            adj[v].add(u)
            deg[u] += 1
            deg[v] += 1
            
        leaves = [i for i in range(n) if deg[i] == 1]
        heapq.heapify(leaves)
        
        seq = []
        for _ in range(n - 2):
            leaf = heapq.heappop(leaves)
            nb = next(iter(adj[leaf]))
            seq.append(nb)
            adj[leaf].remove(nb)
            adj[nb].remove(leaf)
            deg[nb] -= 1
            if deg[nb] == 1:
                heapq.heappush(leaves, nb)
                
        sys.stdout.write(" ".join(map(str, seq)) + "\n")
    else:
        n = int(tokens[1])
        seq = [int(tokens[2 + i]) for i in range(max(0, n - 2))]
        deg = [1] * n
        for v in seq:
            deg[v] += 1
            
        leaves = [i for i in range(n) if deg[i] == 1]
        heapq.heapify(leaves)
        
        edges = []
        for v in seq:
            leaf = heapq.heappop(leaves)
            edges.append((min(leaf, v), max(leaf, v)))
            deg[v] -= 1
            if deg[v] == 1:
                heapq.heappush(leaves, v)
                
        a = heapq.heappop(leaves)
        b = heapq.heappop(leaves)
        edges.append((min(a, b), max(a, b)))
        edges.sort()
        for u, v in edges:
            sys.stdout.write(f"{u} {v}\n")

if __name__ == "__main__":
    main()
