import sys
from collections import deque

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    idx = 0
    try:
        n_states = int(tokens[idx])
        start_state = int(tokens[idx + 1])
        num_accept = int(tokens[idx + 2])
    except (ValueError, IndexError):
        return
    idx += 3

    nfa_accept = set()
    for _ in range(num_accept):
        nfa_accept.add(int(tokens[idx]))
        idx += 1

    num_transitions = int(tokens[idx])
    idx += 1

    nfa = [[] for _ in range(n_states)]
    alphabet_set = set()
    for _ in range(num_transitions):
        u = int(tokens[idx])
        v = int(tokens[idx + 1])
        c = tokens[idx + 2]
        idx += 3
        nfa[u].append((c, v))
        if c != '#':
            alphabet_set.add(c)

    alphabet = sorted(list(alphabet_set))

    def epsilon_closure(states):
        closure = set(states)
        q = deque(states)
        while q:
            u = q.popleft()
            for ch, to in nfa[u]:
                if ch == '#' and to not in closure:
                    closure.add(to)
                    q.append(to)
        return frozenset(closure)

    def move_states(states, c):
        res = set()
        for s in states:
            for ch, to in nfa[s]:
                if ch == c:
                    res.add(to)
        return res

    start_set = epsilon_closure([start_state])
    dfa_state_map = {start_set: 0}
    dfa_states = [start_set]
    dfa_accept = [any(s in nfa_accept for s in start_set)]
    dfa_trans = [{}]

    work_queue = deque([0])
    while work_queue:
        curr_id = work_queue.popleft()
        curr_set = dfa_states[curr_id]

        for c in alphabet:
            moved = move_states(curr_set, c)
            if not moved:
                continue
            nxt = epsilon_closure(moved)
            if not nxt:
                continue

            if nxt not in dfa_state_map:
                nxt_id = len(dfa_states)
                dfa_state_map[nxt] = nxt_id
                dfa_states.append(nxt)
                dfa_trans.append({})
                dfa_accept.append(any(s in nfa_accept for s in nxt))
                work_queue.append(nxt_id)
            else:
                nxt_id = dfa_state_map[nxt]
            dfa_trans[curr_id][c] = nxt_id

    out = [
        f"DFA states: {len(dfa_states)}",
        f"DFA accept states: {sum(1 for b in dfa_accept if b)}"
    ]

    if idx < len(tokens):
        num_queries = int(tokens[idx])
        idx += 1
        for _ in range(num_queries):
            if idx >= len(tokens):
                break
            w = tokens[idx]
            idx += 1
            if w == "EPS":
                w = ""
            state = 0
            ok = True
            for ch in w:
                if ch not in dfa_trans[state]:
                    ok = False
                    break
                state = dfa_trans[state][ch]
            if ok and dfa_accept[state]:
                out.append("ACCEPT")
            else:
                out.append("REJECT")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
