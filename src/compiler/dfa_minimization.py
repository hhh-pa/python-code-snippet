import sys
from collections import deque

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    idx = 0
    n = int(tokens[idx])
    start_state = int(tokens[idx + 1])
    num_accept = int(tokens[idx + 2])
    idx += 3

    accept_states = set()
    for _ in range(num_accept):
        accept_states.add(int(tokens[idx]))
        idx += 1

    alpha_size = int(tokens[idx])
    idx += 1
    alphabet = []
    for _ in range(alpha_size):
        alphabet.append(tokens[idx])
        idx += 1

    num_trans = int(tokens[idx])
    idx += 1

    trans = [{} for _ in range(n)]
    rev_trans = [{} for _ in range(n)]

    for _ in range(num_trans):
        u = int(tokens[idx])
        v = int(tokens[idx + 1])
        c = tokens[idx + 2]
        idx += 3
        trans[u][c] = v
        rev_trans[v].setdefault(c, []).append(u)

    # Step 1: Reachability
    reachable = [False] * n
    reachable[start_state] = True
    q = deque([start_state])
    while q:
        u = q.popleft()
        for c, v in trans[u].items():
            if not reachable[v]:
                reachable[v] = True
                q.append(v)

    states = [i for i in range(n) if reachable[i]]

    # Step 2: Initial partition
    F = set(s for s in states if s in accept_states)
    nonF = set(s for s in states if s not in accept_states)

    P = []
    W = deque()
    if F:
        P.append(F)
    if nonF:
        P.append(nonF)

    if F and nonF:
        if len(F) <= len(nonF):
            W.append(F)
        else:
            W.append(nonF)
    elif F:
        W.append(F)
    elif nonF:
        W.append(nonF)

    # Step 3: Refinement loop
    while W:
        A = W.popleft()
        for c in alphabet:
            X = set()
            for a in A:
                for u in rev_trans[a].get(c, []):
                    if reachable[u]:
                        X.add(u)
            if not X:
                continue

            new_P = []
            for Y in P:
                inter = Y & X
                diff = Y - X
                if inter and diff:
                    new_P.append(inter)
                    new_P.append(diff)

                    in_W = False
                    next_W = deque()
                    while W:
                        item = W.popleft()
                        if item == Y:
                            in_W = True
                            next_W.append(inter)
                            next_W.append(diff)
                        else:
                            next_W.append(item)
                    W = next_W

                    if not in_W:
                        if len(inter) <= len(diff):
                            W.append(inter)
                        else:
                            W.append(diff)
                else:
                    new_P.append(Y)
            P = new_P

    state_to_part = [-1] * n
    for pid, part in enumerate(P):
        for s in part:
            state_to_part[s] = pid

    min_start = state_to_part[start_state]
    min_accept = set()
    for pid, part in enumerate(P):
        for s in part:
            if s in accept_states:
                min_accept.add(pid)
                break

    out = [f"Minimal DFA states: {len(P)}", f"Accept states: {len(min_accept)}"]

    min_trans = [{} for _ in range(len(P))]
    for pid, part in enumerate(P):
        rep = min(part)
        for c, v in trans[rep].items():
            if reachable[v]:
                min_trans[pid][c] = state_to_part[v]

    if idx < len(tokens):
        num_queries = int(tokens[idx])
        idx += 1
        for _ in range(num_queries):
            w = tokens[idx]
            idx += 1
            if w == "EPS":
                w = ""
            curr = min_start
            ok = True
            for ch in w:
                if curr < 0 or curr >= len(min_trans):
                    ok = False
                    break
                if ch not in min_trans[curr]:
                    ok = False
                    break
                curr = min_trans[curr][ch]
            if ok and curr in min_accept:
                out.append("ACCEPT")
            else:
                out.append("REJECT")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
