import sys


def morris_inorder(val, left, right):
    curr = 0
    res = []
    # Make a copy of right because morris mutates right array
    r = list(right)
    while curr != -1:
        if left[curr] == -1:
            res.append(str(val[curr]))
            curr = r[curr]
        else:
            pred = left[curr]
            while r[pred] != -1 and r[pred] != curr:
                pred = r[pred]
            if r[pred] == -1:
                r[pred] = curr
                curr = left[curr]
            else:
                r[pred] = -1
                res.append(str(val[curr]))
                curr = r[curr]
    return " ".join(res)


def morris_preorder(val, left, right):
    curr = 0
    res = []
    r = list(right)
    while curr != -1:
        if left[curr] == -1:
            res.append(str(val[curr]))
            curr = r[curr]
        else:
            pred = left[curr]
            while r[pred] != -1 and r[pred] != curr:
                pred = r[pred]
            if r[pred] == -1:
                res.append(str(val[curr]))
                r[pred] = curr
                curr = left[curr]
            else:
                r[pred] = -1
                curr = r[curr]
    return " ".join(res)


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    if n <= 0:
        return

    val = [0] * n
    left = [-1] * n
    right = [-1] * n
    idx = 1
    for i in range(n):
        val[i] = int(tokens[idx])
        left[i] = int(tokens[idx + 1])
        right[i] = int(tokens[idx + 2])
        idx += 3

    sys.stdout.write(morris_inorder(val, left, right) + "\n")
    sys.stdout.write(morris_preorder(val, left, right) + "\n")


if __name__ == "__main__":
    main()
