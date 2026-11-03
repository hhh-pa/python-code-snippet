import sys


class XorList:
    def __init__(self):
        self.val = []
        self.link = []
        self.head = -1
        self.tail = -1

    def alloc(self, x):
        n = len(self.val)
        self.val.append(x)
        self.link.append(0)
        return n

    def push_front(self, x):
        n = self.alloc(x)
        self.link[n] = 0 ^ (self.head + 1)
        if self.head == -1:
            self.head = self.tail = n
            return
        self.link[self.head] = self.link[self.head] ^ (n + 1)
        self.head = n

    def push_back(self, x):
        n = self.alloc(x)
        self.link[n] = (self.tail + 1) ^ 0
        if self.tail == -1:
            self.head = self.tail = n
            return
        self.link[self.tail] = self.link[self.tail] ^ (n + 1)
        self.tail = n

    def pop_front(self):
        if self.head == -1:
            return None
        o = self.val[self.head]
        nxt = self.link[self.head] ^ 0
        if nxt == 0:
            self.head = self.tail = -1
            return o
        ni = nxt - 1
        self.link[ni] = self.link[ni] ^ (self.head + 1)
        self.head = ni
        return o

    def pop_back(self):
        if self.tail == -1:
            return None
        o = self.val[self.tail]
        prv = self.link[self.tail] ^ 0
        if prv == 0:
            self.head = self.tail = -1
            return o
        pi = prv - 1
        self.link[pi] = self.link[pi] ^ (self.tail + 1)
        self.tail = pi
        return o

    def print_list(self):
        res = []
        prev = -1
        cur = self.head
        while cur != -1:
            res.append(str(self.val[cur]))
            nxt = self.link[cur] ^ (prev + 1)
            prev = cur
            cur = -1 if nxt == 0 else nxt - 1
        return " ".join(res)


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    q = int(tokens[0])
    idx = 1
    l = XorList()
    out = []
    for _ in range(q):
        op = int(tokens[idx])
        idx += 1
        if op == 1:
            x = int(tokens[idx])
            idx += 1
            l.push_front(x)
        elif op == 2:
            x = int(tokens[idx])
            idx += 1
            l.push_back(x)
        elif op == 3:
            res = l.pop_front()
            out.append(str(res) if res is not None else "EMPTY")
        elif op == 4:
            res = l.pop_back()
            out.append(str(res) if res is not None else "EMPTY")
        elif op == 5:
            out.append(l.print_list())

    sys.stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
