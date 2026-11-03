import sys

sys.setrecursionlimit(200000)

class SuffixNode:
    __slots__ = ('children', 'suffix_link', 'start', 'end', 'is_leaf')
    def __init__(self, start=0, end=-1, is_leaf=False):
        self.children = {}
        self.suffix_link = 0
        self.start = start
        self.end = end
        self.is_leaf = is_leaf

class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.tree = [SuffixNode(0, -1, False)]
        self.root = 0
        self.active_node = 0
        self.active_edge = -1
        self.active_length = 0
        self.remaining_suffix_count = 0
        self.leaf_end = -1

        for i in range(len(text)):
            self.extend(i)

    def new_node(self, start, end, is_leaf):
        node = SuffixNode(start, end, is_leaf)
        node.suffix_link = self.root
        self.tree.append(node)
        return len(self.tree) - 1

    def get_end(self, n_idx):
        node = self.tree[n_idx]
        if node.is_leaf:
            return self.leaf_end
        return node.end

    def edge_length(self, n_idx):
        if n_idx == self.root:
            return 0
        return self.get_end(n_idx) - self.tree[n_idx].start + 1

    def walk_down(self, curr_node):
        elen = self.edge_length(curr_node)
        if self.active_length >= elen:
            self.active_edge += elen
            self.active_length -= elen
            self.active_node = curr_node
            return True
        return False

    def extend(self, pos):
        self.leaf_end = pos
        self.remaining_suffix_count += 1
        last_new_node = -1

        while self.remaining_suffix_count > 0:
            if self.active_length == 0:
                self.active_edge = pos

            cur_char = self.text[self.active_edge]
            if cur_char not in self.tree[self.active_node].children:
                leaf = self.new_node(pos, -1, True)
                self.tree[self.active_node].children[cur_char] = leaf

                if last_new_node != -1:
                    self.tree[last_new_node].suffix_link = self.active_node
                    last_new_node = -1
            else:
                next_node = self.tree[self.active_node].children[cur_char]
                if self.walk_down(next_node):
                    continue

                edge_char_pos = self.tree[next_node].start + self.active_length
                if self.text[edge_char_pos] == self.text[pos]:
                    if last_new_node != -1 and self.active_node != self.root:
                        self.tree[last_new_node].suffix_link = self.active_node
                        last_new_node = -1
                    self.active_length += 1
                    break

                split_end = self.tree[next_node].start + self.active_length - 1
                split = self.new_node(self.tree[next_node].start, split_end, False)
                self.tree[self.active_node].children[cur_char] = split

                leaf = self.new_node(pos, -1, True)
                self.tree[split].children[self.text[pos]] = leaf

                self.tree[next_node].start += self.active_length
                self.tree[split].children[self.text[edge_char_pos]] = next_node

                if last_new_node != -1:
                    self.tree[last_new_node].suffix_link = split
                last_new_node = split

            self.remaining_suffix_count -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remaining_suffix_count + 1
            elif self.active_node != self.root:
                self.active_node = self.tree[self.active_node].suffix_link

    def node_count(self):
        return len(self.tree)

    def count_distinct_substrings(self, u=0):
        count = 0
        for v in self.tree[u].children.values():
            elen = self.get_end(v) - self.tree[v].start + 1
            count += elen + self.count_distinct_substrings(v)
        return count

    def find_pattern(self, pat):
        cur = self.root
        idx = 0
        while idx < len(pat):
            c = pat[idx]
            if c not in self.tree[cur].children:
                return False
            nxt = self.tree[cur].children[c]
            start = self.tree[nxt].start
            end = self.get_end(nxt)
            edge_len = end - start + 1

            for k in range(edge_len):
                if idx >= len(pat):
                    break
                if self.text[start + k] != pat[idx]:
                    return False
                idx += 1
            cur = nxt
        return True

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    s = next(it)

    st = SuffixTree(s)
    out = [
        f"Nodes: {st.node_count()}",
        f"Distinct substrings: {st.count_distinct_substrings(0)}"
    ]

    try:
        num_queries = int(next(it))
        for _ in range(num_queries):
            pat = next(it)
            out.append("YES" if st.find_pattern(pat) else "NO")
    except StopIteration:
        pass

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
