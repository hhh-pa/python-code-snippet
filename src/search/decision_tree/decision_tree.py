import sys
import math

class Node:
    __slots__ = ('leaf', 'label', 'feat', 'depth', 'l', 'r')
    def __init__(self, depth=0):
        self.leaf = False
        self.label = 0
        self.feat = 0
        self.depth = depth
        self.l = None
        self.r = None

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    
    try:
        T_str = next(it)
    except StopIteration:
        return
    T = int(T_str)
    
    out = []
    for _ in range(T):
        N = int(next(it))
        F = int(next(it))
        D = int(next(it))
        
        X = []
        Y = []
        for _ in range(N):
            row = [int(next(it)) for _ in range(F)]
            y = int(next(it))
            X.append(row)
            Y.append(y)
            
        def entropy(idx):
            if not idx:
                return 0.0
            c = sum(1 for i in idx if Y[i] == 1)
            p = c / len(idx)
            if p == 0.0 or p == 1.0:
                return 0.0
            return -(p * math.log(p) + (1.0 - p) * math.log(1.0 - p))
            
        def build(idx, used, depth, pmaj):
            c0, c1 = 0, 0
            for i in idx:
                if Y[i] == 1:
                    c1 += 1
                else:
                    c0 += 1
            nd = Node(depth)
            if not idx:
                nd.leaf = True
                nd.label = pmaj
                return nd
            if c0 == 0 or c1 == 0 or depth >= D or used == (1 << F) - 1:
                nd.leaf = True
                nd.label = 1 if c1 >= c0 else 0
                return nd
                
            base = entropy(idx)
            bf = 0
            bg = -1.0
            n_idx = len(idx)
            for f in range(F):
                if (used >> f) & 1:
                    continue
                L = []
                R = []
                for i in idx:
                    if X[i][f] == 0:
                        L.append(i)
                    else:
                        R.append(i)
                g = base - (len(L) / n_idx) * entropy(L) - (len(R) / n_idx) * entropy(R)
                if g > bg + 1e-12:
                    bg = g
                    bf = f
                    
            maj = 1 if c1 >= c0 else 0
            L = []
            R = []
            for i in idx:
                if X[i][bf] == 0:
                    L.append(i)
                else:
                    R.append(i)
            nd.leaf = False
            nd.feat = bf
            nd.l = build(L, used | (1 << bf), depth + 1, maj)
            nd.r = build(R, used | (1 << bf), depth + 1, maj)
            return nd
            
        def predict(nd, x):
            while not nd.leaf:
                nd = nd.l if x[nd.feat] == 0 else nd.r
            return nd.label
            
        def maxdepth(nd):
            if nd.leaf:
                return nd.depth
            return max(maxdepth(nd.l), maxdepth(nd.r))
            
        all_indices = list(range(N))
        root = build(all_indices, 0, 0, 1)
        out.append(f"DT {maxdepth(root)}")
        preds = [str(predict(root, X[i])) for i in range(N)]
        out.append(" ".join(preds))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
