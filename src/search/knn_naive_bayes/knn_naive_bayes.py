import sys
import math

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
        k = int(next(it))
        
        X = []
        Y = []
        for _ in range(N):
            row = [int(next(it)) for _ in range(F)]
            y = int(next(it))
            X.append(row)
            Y.append(y)
            
        M = int(next(it))
        Z = []
        for _ in range(M):
            Z.append([int(next(it)) for _ in range(F)])
            
        # KNN
        knn_preds = []
        for t in range(M):
            zt = Z[t]
            d = []
            for i in range(N):
                xi = X[i]
                s = sum((zt[f] - xi[f]) ** 2 for f in range(F))
                d.append((s, i))
            d.sort()
            
            votes = {}
            for j in range(min(k, N)):
                lab = Y[d[j][1]]
                votes[lab] = votes.get(lab, 0) + 1
                
            bl = -1
            bc = -1
            for lab in sorted(votes.keys()):
                if votes[lab] > bc:
                    bc = votes[lab]
                    bl = lab
            knn_preds.append(str(bl))
            
        out.append("KNN " + " ".join(knn_preds))
        
        # Naive Bayes
        classes = sorted(set(Y))
        vmax = [max(X[i][f] for i in range(N)) for f in range(F)]
        
        # Precompute counts for each class:
        # cc: count of Y[i] == c
        # count of X[i][f] == val for Y[i] == c
        class_indices = {c: [i for i in range(N) if Y[i] == c] for c in classes}
        cc_map = {c: len(class_indices[c]) for c in classes}
        
        # To make it fast:
        # feature_counts[c][f][val] = count
        feature_counts = {}
        for c in classes:
            feature_counts[c] = [{} for _ in range(F)]
            for i in class_indices[c]:
                for f in range(F):
                    v = X[i][f]
                    feature_counts[c][f][v] = feature_counts[c][f].get(v, 0) + 1
                    
        nb_preds = []
        for t in range(M):
            zt = Z[t]
            bl = classes[0]
            bs = -1e300
            for c in classes:
                cc = cc_map[c]
                s = math.log(cc / N)
                for f in range(F):
                    cnt = feature_counts[c][f].get(zt[f], 0)
                    s += math.log((cnt + 1) / (cc + vmax[f] + 1))
                if s > bs + 1e-12:
                    bs = s
                    bl = c
            nb_preds.append(str(bl))
            
        out.append("NB " + " ".join(nb_preds))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
