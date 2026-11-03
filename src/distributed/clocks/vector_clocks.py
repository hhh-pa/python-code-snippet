import sys

def compare_clocks(a, b):
    a_le_b = True
    b_le_a = True
    for x, y in zip(a, b):
        if x > y:
            a_le_b = False
        if y > x:
            b_le_a = False
    if a_le_b and b_le_a:
        return 2
    if a_le_b:
        return 1
    if b_le_a:
        return -1
    return 0

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    try:
        n_procs = int(next(it))
        n_ops = int(next(it))
    except StopIteration:
        return

    vc = [[0] * n_procs for _ in range(n_procs)]
    event_clocks = {}
    in_flight_messages = {}

    for _ in range(n_ops):
        op = next(it)
        if op == "LOCAL":
            p = int(next(it))
            name = next(it)
            vc[p][p] += 1
            event_clocks[name] = list(vc[p])
        elif op == "SEND":
            from_p = int(next(it))
            msg_id = next(it)
            vc[from_p][from_p] += 1
            in_flight_messages[msg_id] = list(vc[from_p])
            event_clocks[msg_id + "_SEND"] = list(vc[from_p])
        elif op == "RECV":
            to_p = int(next(it))
            msg_id = next(it)
            msg_vc = in_flight_messages[msg_id]
            for k in range(n_procs):
                if msg_vc[k] > vc[to_p][k]:
                    vc[to_p][k] = msg_vc[k]
            vc[to_p][to_p] += 1
            event_clocks[msg_id + "_RECV"] = list(vc[to_p])

    out = []
    try:
        n_queries = int(next(it))
        for _ in range(n_queries):
            e1 = next(it)
            e2 = next(it)
            v1 = event_clocks[e1]
            v2 = event_clocks[e2]
            rel = compare_clocks(v1, v2)
            if rel == 1:
                out.append(f"{e1} -> {e2}")
            elif rel == -1:
                out.append(f"{e2} -> {e1}")
            elif rel == 2:
                out.append(f"{e1} == {e2}")
            else:
                out.append(f"{e1} || {e2}")
    except StopIteration:
        pass

    if out:
        sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
