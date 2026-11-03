import sys

sys.setrecursionlimit(200000)


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def insert(root, data):
    if root is None:
        return Node(data)
    curr = root
    while True:
        if data <= curr.data:
            if curr.left is None:
                curr.left = Node(data)
                break
            curr = curr.left
        else:
            if curr.right is None:
                curr.right = Node(data)
                break
            curr = curr.right
    return root


def lca(root, v1, v2):
    curr = root
    while curr:
        if v1 < curr.data and v2 < curr.data:
            curr = curr.left
        elif v1 > curr.data and v2 > curr.data:
            curr = curr.right
        else:
            return curr
    return None


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    root = None
    for i in range(n):
        root = insert(root, int(tokens[1 + i]))
    v1 = int(tokens[1 + n])
    v2 = int(tokens[2 + n])
    ans = lca(root, v1, v2)
    if ans:
        sys.stdout.write(f"{ans.data}\n")


if __name__ == "__main__":
    main()
