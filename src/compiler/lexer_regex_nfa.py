import sys

def insert_concat(regex):
    res = []
    n = len(regex)
    for i in range(n):
        c1 = regex[i]
        res.append(c1)
        if i + 1 < n:
            c2 = regex[i + 1]
            c1_can_end = (c1.isalnum() or c1 == '*' or c1 == ')')
            c2_can_start = (c2.isalnum() or c2 == '(')
            if c1_can_end and c2_can_start:
                res.append('.')
    return "".join(res)

def get_prec(c):
    if c == '*':
        return 3
    if c == '.':
        return 2
    if c == '|':
        return 1
    return 0

def to_postfix(infix):
    postfix = []
    op_stack = []
    for c in infix:
        if c.isalnum():
            postfix.append(c)
        elif c == '(':
            op_stack.append(c)
        elif c == ')':
            while op_stack and op_stack[-1] != '(':
                postfix.append(op_stack.pop())
            if op_stack:
                op_stack.pop()
        else:
            while op_stack and op_stack[-1] != '(' and get_prec(op_stack[-1]) >= get_prec(c):
                postfix.append(op_stack.pop())
            op_stack.append(c)
    while op_stack:
        postfix.append(op_stack.pop())
    return "".join(postfix)

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    pattern = tokens[0]
    infix = insert_concat(pattern)
    postfix = to_postfix(infix)

    nfa = []  # list of list of (ch, to)

    def add_state():
        nfa.append([])
        return len(nfa) - 1

    def add_trans(u, v, ch):
        nfa[u].append((ch, v))

    st = []
    for c in postfix:
        if c == '.':
            f2_start, f2_end = st.pop()
            f1_start, f1_end = st.pop()
            add_trans(f1_end, f2_start, None)
            st.append((f1_start, f2_end))
        elif c == '|':
            f2_start, f2_end = st.pop()
            f1_start, f1_end = st.pop()
            s = add_state()
            e = add_state()
            add_trans(s, f1_start, None)
            add_trans(s, f2_start, None)
            add_trans(f1_end, e, None)
            add_trans(f2_end, e, None)
            st.append((s, e))
        elif c == '*':
            f_start, f_end = st.pop()
            s = add_state()
            e = add_state()
            add_trans(s, f_start, None)
            add_trans(s, e, None)
            add_trans(f_end, f_start, None)
            add_trans(f_end, e, None)
            st.append((s, e))
        else:
            s = add_state()
            e = add_state()
            add_trans(s, e, c)
            st.append((s, e))

    frag_start, frag_end = st[-1]

    def get_closure(start_states):
        closure = set(start_states)
        stack = list(start_states)
        while stack:
            u = stack.pop()
            for ch, to in nfa[u]:
                if ch is None and to not in closure:
                    closure.add(to)
                    stack.append(to)
        return closure

    idx = 1
    if idx >= len(tokens):
        return
    k = int(tokens[idx])
    idx += 1

    out = []
    for _ in range(k):
        if idx >= len(tokens):
            break
        test_str = tokens[idx]
        idx += 1
        if test_str == "EPS":
            test_str = ""

        current = get_closure([frag_start])
        matched = True
        for c in test_str:
            next_base = []
            for state in current:
                for ch, to in nfa[state]:
                    if ch == c:
                        next_base.append(to)
            current = get_closure(next_base)
            if not current:
                matched = False
                break
        if matched and (frag_end in current):
            out.append("MATCH")
        else:
            out.append("NO_MATCH")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
