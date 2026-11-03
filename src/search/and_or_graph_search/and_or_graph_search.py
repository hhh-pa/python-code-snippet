import sys

sys.setrecursionlimit(200000)

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
        n = int(next(it))
        typ = [int(next(it)) for _ in range(n)]
        children = [[] for _ in range(n)]
        for i in range(n):
            if typ[i] == 0 or typ[i] == 1:
                k = int(next(it))
                children[i] = [int(next(it)) for _ in range(k)]
                
        memo = [-1] * n
        memo_plan = [None] * n
        
        def solve(node):
            if memo[node] != -1:
                if memo[node] == 0:
                    return None, False
                return set(memo_plan[node]), True
            
            if typ[node] == 2:
                memo[node] = 1
                memo_plan[node] = {node}
                return {node}, True
            
            if typ[node] == 3:
                memo[node] = 0
                return None, False
                
            if typ[node] == 1: # AND
                combined = {node}
                for c in children[node]:
                    sub, ok = solve(c)
                    if not ok:
                        memo[node] = 0
                        return None, False
                    combined |= sub
                memo[node] = 1
                memo_plan[node] = set(combined)
                return combined, True
                
            # OR (typ[node] == 0)
            for c in children[node]:
                sub, ok = solve(c)
                if ok:
                    combined = {node} | sub
                    memo[node] = 1
                    memo_plan[node] = set(combined)
                    return combined, True
                    
            memo[node] = 0
            return None, False

        res, ok = solve(0)
        if not ok:
            out.append("UNSOLVABLE")
        else:
            ks = sorted(res)
            out.append(f"SOLVABLE {len(ks)}")
            out.append(" ".join(map(str, ks)))
            
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
