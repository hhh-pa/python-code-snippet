import sys

class State:
    __slots__ = ('len', 'link', 'next')
    def __init__(self, length=0, link=-1):
        self.len = length
        self.link = link
        self.next = {}

class SuffixAutomaton:
    def __init__(self):
        self.st = [State(0, -1)]
        self.last = 0

    def extend(self, c):
        cur = len(self.st)
        self.st.append(State(self.st[self.last].len + 1))

        p = self.last
        while p != -1 and c not in self.st[p].next:
            self.st[p].next[c] = cur
            p = self.st[p].link

        if p == -1:
            self.st[cur].link = 0
        else:
            q = self.st[p].next[c]
            if self.st[p].len + 1 == self.st[q].len:
                self.st[cur].link = q
            else:
                clone = len(self.st)
                clone_state = State(self.st[p].len + 1, self.st[q].link)
                clone_state.next = self.st[q].next.copy()
                self.st.append(clone_state)

                while p != -1 and self.st[p].next.get(c) == q:
                    self.st[p].next[c] = clone
                    p = self.st[p].link

                self.st[q].link = clone
                self.st[cur].link = clone
        self.last = cur

    def state_count(self):
        return len(self.st)

    def transition_count(self):
        return sum(len(s.next) for s in self.st)

    def distinct_substrings(self):
        total = 0
        for i in range(1, len(self.st)):
            link_len = 0 if self.st[i].link == -1 else self.st[self.st[i].link].len
            total += self.st[i].len - link_len
        return total

    def contains(self, pat):
        cur = 0
        for c in pat:
            if c not in self.st[cur].next:
                return False
            cur = self.st[cur].next[c]
        return True

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    s = next(it)

    sam = SuffixAutomaton()
    for c in s:
        sam.extend(c)

    out = [
        f"States: {sam.state_count()}",
        f"Transitions: {sam.transition_count()}",
        f"Distinct substrings: {sam.distinct_substrings()}"
    ]

    try:
        num_queries = int(next(it))
        for _ in range(num_queries):
            pat = next(it)
            out.append("YES" if sam.contains(pat) else "NO")
    except StopIteration:
        pass

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
