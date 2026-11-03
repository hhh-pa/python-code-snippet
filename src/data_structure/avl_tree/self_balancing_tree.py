import sys

sys.setrecursionlimit(200000)


class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.ht = 0


def height(node):
    return node.ht if node else -1


def update_ht(node):
    if node:
        hl = height(node.left)
        hr = height(node.right)
        node.ht = 1 + (hl if hl > hr else hr)


def balance_factor(node):
    return (height(node.left) - height(node.right)) if node else 0


def rotate_right(y):
    x = y.left
    t2 = x.right
    x.right = y
    y.left = t2
    update_ht(y)
    update_ht(x)
    return x


def rotate_left(x):
    y = x.right
    t2 = y.left
    y.left = x
    x.right = t2
    update_ht(x)
    update_ht(y)
    return y


def insert(node, val):
    if not node:
        return Node(val)
    if val < node.val:
        node.left = insert(node.left, val)
    else:
        node.right = insert(node.right, val)
    update_ht(node)
    bf = balance_factor(node)
    if bf > 1:
        if val > node.left.val:
            node.left = rotate_left(node.left)
        return rotate_right(node)
    if bf < -1:
        if val < node.right.val:
            node.right = rotate_right(node.right)
        return rotate_left(node)
    return node


def inorder_tokens(root, out):
    if not root:
        return
    inorder_tokens(root.left, out)
    out.append(f"{root.val}(BF={balance_factor(root)}) ")
    inorder_tokens(root.right, out)


def preorder_tokens(root, out):
    if not root:
        return
    out.append(f"{root.val}(BF={balance_factor(root)}) ")
    preorder_tokens(root.left, out)
    preorder_tokens(root.right, out)


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    n = int(tokens[0])
    root = None
    for i in range(n):
        root = insert(root, int(tokens[1 + i]))
    if 1 + n < len(tokens):
        new_val = int(tokens[1 + n])
        root = insert(root, new_val)

    inorder = []
    inorder_tokens(root, inorder)
    preorder = []
    preorder_tokens(root, preorder)

    sys.stdout.write("".join(inorder) + "\n")
    sys.stdout.write("".join(preorder) + "\n")


if __name__ == "__main__":
    main()
