import sys

class Trie:
    def __init__(self):
        self.root = {}

    def add_word(self, w):
        curr = self.root
        is_bad = False
        for c in w:
            if c not in curr:
                curr[c] = {}
            curr = curr[c]
            if '__end__' in curr:
                is_bad = True
        if len(curr) > 0 and '__end__' not in curr:
            is_bad = True
        curr['__end__'] = True
        return is_bad

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    n = int(next(it))
    trie = Trie()
    for _ in range(n):
        s = next(it)
        if trie.add_word(s):
            print("BAD SET")
            print(s)
            return
    print("GOOD SET")

if __name__ == "__main__":
    main()
