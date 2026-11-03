import itertools
import sys

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    mode = tokens[0]
    idx = 1
    if mode == "purged":
        P = int(tokens[idx])
        E = int(tokens[idx + 1])
        K = 1
        idx += 2
    else:
        P = int(tokens[idx])
        K = int(tokens[idx + 1])
        E = int(tokens[idx + 2])
        idx += 3
        
    L = int(tokens[idx])
    idx += 1
    t0 = []
    t1 = []
    for _ in range(L):
        t0.append(int(tokens[idx]))
        t1.append(int(tokens[idx + 1]))
        idx += 2
        
    parts = [[] for _ in range(P)]
    for j in range(L):
        parts[j * P // L].append(j)
        
    tests = []
    if mode == "purged":
        for f in range(P):
            tests.append(parts[f])
    else:
        for comb in itertools.combinations(range(P), K):
            t = []
            for c in comb:
                t.extend(parts[c])
            tests.append(t)
            
    tag = "FOLD " if mode == "purged" else "SPLIT "
    for s, test in enumerate(tests):
        is_test = set(test)
        train = [j for j in range(L) if j not in is_test]
        tmin = min(t0[x] for x in test)
        tmax = max(t1[x] for x in test)
        kept = []
        for j in train:
            if not (t1[j] < tmin or t0[j] > tmax):
                continue
            if t0[j] > tmax and t0[j] <= tmax + E:
                continue
            kept.append(j)
            
        train_str = ",".join(str(x) for x in kept) if kept else "-"
        test_str = ",".join(str(x) for x in test) if test else "-"
        sys.stdout.write(f"{tag}{s}: train={train_str} test={test_str}\n")

if __name__ == "__main__":
    main()
