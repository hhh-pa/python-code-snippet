import sys

prods = [
    ("", 0),
    ("E -> E + T", 3),
    ("E -> T", 1),
    ("T -> T * F", 3),
    ("T -> F", 1),
    ("F -> ( E )", 3),
    ("F -> id", 1)
]

action_table = {
    (0, "id"): 5,
    (0, "("): 4,
    (1, "+"): 6,
    (1, "$"): 1000,
    (2, "+"): -2,
    (2, "*"): 7,
    (2, ")"): -2,
    (2, "$"): -2,
    (3, "+"): -4,
    (3, "*"): -4,
    (3, ")"): -4,
    (3, "$"): -4,
    (4, "id"): 5,
    (4, "("): 4,
    (5, "+"): -6,
    (5, "*"): -6,
    (5, ")"): -6,
    (5, "$"): -6,
    (6, "id"): 5,
    (6, "("): 4,
    (7, "id"): 5,
    (7, "("): 4,
    (8, "+"): 6,
    (8, ")"): 11,
    (9, "+"): -1,
    (9, "*"): 7,
    (9, ")"): -1,
    (9, "$"): -1,
    (10, "+"): -3,
    (10, "*"): -3,
    (10, ")"): -3,
    (10, "$"): -3,
    (11, "+"): -5,
    (11, "*"): -5,
    (11, ")"): -5,
    (11, "$"): -5,
}

goto_table = {
    (0, "E"): 1,
    (0, "T"): 2,
    (0, "F"): 3,
    (4, "E"): 8,
    (4, "T"): 2,
    (4, "F"): 3,
    (6, "T"): 9,
    (6, "F"): 3,
    (7, "F"): 10,
}

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    if tokens[-1] != "$":
        tokens.append("$")

    state_stack = [0]
    ip = 0
    out = []

    while True:
        s = state_stack[-1]
        a = tokens[ip]
        if (s, a) not in action_table:
            out.append("SYNTAX_ERROR")
            break
        act = action_table[(s, a)]
        if act == 1000:
            out.append("ACCEPTED")
            break
        elif act > 0:
            state_stack.append(act)
            ip += 1
        elif act < 0:
            prod_idx = -act
            out.append(prods[prod_idx][0])
            for _ in range(prods[prod_idx][1]):
                state_stack.pop()
            t = state_stack[-1]
            lhs = prods[prod_idx][0][0]
            if (t, lhs) not in goto_table:
                out.append("SYNTAX_ERROR")
                break
            state_stack.append(goto_table[(t, lhs)])
        else:
            out.append("SYNTAX_ERROR")
            break

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
