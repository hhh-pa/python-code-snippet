# https://www.hackerrank.com/challenges/binary-search-tree-insertion/problem
import sys


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def insert(root, data):
    if root is None:
        return Node(data)
    if data <= root.data:
        root.left = insert(root.left, data)
    else:
        root.right = insert(root.right, data)
    return root


def preorder(root, out):
    if root is None:
        return
    out.append(str(root.data))
    preorder(root.left, out)
    preorder(root.right, out)


def main():
    data = list(map(int, sys.stdin.read().split()))
    if not data or data[0] < 0:
        return
    n = data[0]
    root = None
    for v in data[1:1 + n]:
        root = insert(root, v)
    out = []
    preorder(root, out)
    sys.stdout.write(' '.join(out) + ' ' if out else '')


if __name__ == '__main__':
    main()
