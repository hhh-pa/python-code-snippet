"""Meta-labeling: correctness + fixed-tree size (AFML ch 3)."""

import sys


def main():
    toks = sys.stdin.read().split()
    if not toks:
        return
    e = int(toks[0])
    f = int(toks[1])
    idx = 2
    sides = [0] * e
    feats = [[0.0] * f for _ in range(e)]
    labels = [0] * e
    for i in range(e):
        sides[i] = int(toks[idx])
        for j in range(f):
            feats[i][j] = float(toks[idx + 1 + j])
        labels[i] = int(toks[idx + 1 + f])
        idx += 2 + f
    t = int(toks[idx])
    idx += 1
    nodes = []
    for _ in range(t):
        if toks[idx] == "LEAF":
            nodes.append((0, float(toks[idx + 1]), 0, 0, 0))
            idx += 2
        else:
            nodes.append(
                (
                    1,
                    0.0,
                    int(toks[idx + 1]),
                    float(toks[idx + 2]),
                    int(toks[idx + 3]),
                    int(toks[idx + 4]),
                )
            )
            idx += 5
    out = []
    good = 0
    for i in range(e):
        y = 1 if (sides[i] == labels[i] and labels[i] != 0) else 0
        good += y
        node = 0
        while nodes[node][0] == 1:
            _, _, feat, thr, left, right = nodes[node]
            node = left if feats[i][feat] <= thr else right
        out.append(f"META {y} SIZE {nodes[node][1]:.6f}")
    out.append(f"ACC {good / e:.6f}")
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
