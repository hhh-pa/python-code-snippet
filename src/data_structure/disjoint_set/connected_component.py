import sys


def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    parent = list(range(n))
    root_number = n

    def find(i):
        root = i
        while parent[root] != root:
            root = parent[root]
        curr = i
        while curr != root:
            nxt = parent[curr]
            parent[curr] = root
            curr = nxt
        return root

    out = []
    idx = 1
    total_tokens = len(input_data)
    while idx + 1 < total_tokens:
        u = int(input_data[idx]) - 1
        v = int(input_data[idx + 1]) - 1
        idx += 2
        u_root = find(u)
        v_root = find(v)
        if u_root != v_root:
            parent[v_root] = u_root
            root_number -= 1
            out.append(str(root_number))
        else:
            out.append(f"{root_number} CYCLE FORMED!")

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
