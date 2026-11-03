import sys
import heapq

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    fr = [int(tokens[1 + i]) for i in range(n)]
    if n == 1:
        print(0)
        print(0)
        return
        
    F = list(fr)
    MS = list(range(n))
    L = [-1] * n
    R = [-1] * n
    pq = []
    for i in range(n):
        heapq.heappush(pq, (fr[i], i, i))
        
    while len(pq) > 1:
        f1, m1, a = heapq.heappop(pq)
        f2, m2, b = heapq.heappop(pq)
        nid = len(F)
        F.append(f1 + f2)
        min_m = min(m1, m2)
        MS.append(min_m)
        L.append(a)
        R.append(b)
        heapq.heappush(pq, (f1 + f2, min_m, nid))
        
    root = pq[0][2]
    dd = [0] * len(F)
    st = [root]
    while st:
        u = st.pop()
        if L[u] != -1:
            dd[L[u]] = dd[u] + 1
            dd[R[u]] = dd[u] + 1
            st.append(L[u])
            st.append(R[u])
            
    cost = sum(fr[i] * dd[i] for i in range(n))
    print(cost)
    print(*(dd[:n]))

if __name__ == '__main__':
    main()
