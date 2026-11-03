import sys
import math

MASK64 = 0xFFFFFFFFFFFFFFFF
MULT = 6364136223846793005
ADD = 1442695040888963407

class LCG:
    def __init__(self, s):
        self.s = s & MASK64

    def next(self):
        self.s = (self.s * MULT + ADD) & MASK64
        return self.s

    def next_int(self, n):
        return int(self.next() % n)

class Node:
    __slots__ = ('stones', 'player', 'visits', 'wins', 'moves', 'kids')
    def __init__(self, stones, player):
        self.stones = stones
        self.player = player
        self.visits = 0
        self.wins = 0
        self.moves = []
        self.kids = []

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    
    try:
        T_str = next(it)
    except StopIteration:
        return
    T = int(T_str)
    
    out = []
    for _ in range(T):
        N = int(next(it))
        K = int(next(it))
        I = int(next(it))
        seed = int(next(it)) & MASK64
        
        rng = LCG(seed)
        tree = []
        root = Node(N, 0)
        root.moves = [m for m in range(1, min(K, N) + 1)]
        tree.append(root)
        
        for _ in range(I):
            v = 0
            traj = [0]
            while True:
                nd = tree[v]
                if nd.stones == 0:
                    break
                if len(nd.kids) < len(nd.moves):
                    mv = nd.moves[len(nd.kids)]
                    ch = Node(nd.stones - mv, 1 - nd.player)
                    ch.moves = [m for m in range(1, min(K, ch.stones) + 1)]
                    nd.kids.append(len(tree))
                    tree.append(ch)
                    v = len(tree) - 1
                    traj.append(v)
                    break
                lN = math.log(nd.visits)
                bi = 0
                bu = -1e300
                for i, kid_idx in enumerate(nd.kids):
                    c = tree[kid_idx]
                    u = 1.0 - c.wins / c.visits + math.sqrt(2.0 * lN / c.visits)
                    if u > bu:
                        bu = u
                        bi = i
                v = nd.kids[bi]
                traj.append(v)
                
            st = tree[v].stones
            pl = tree[v].player
            while st > 0:
                nm = min(K, st)
                pick = rng.next_int(nm)
                mv = pick + 1
                st -= mv
                pl = 1 - pl
                
            winner = 1 - pl
            for idx in traj:
                tree[idx].visits += 1
                if tree[idx].player == winner:
                    tree[idx].wins += 1
                    
        rt = tree[0]
        best = rt.moves[0]
        bv = -1
        for kid_idx in rt.kids:
            c = tree[kid_idx]
            mv = rt.stones - c.stones
            if c.visits > bv:
                bv = c.visits
                best = mv
                
        row = [f"MCTS {best} V"]
        for kid_idx in rt.kids:
            row.append(str(tree[kid_idx].visits))
        row.append("W")
        for kid_idx in rt.kids:
            row.append(str(tree[kid_idx].wins))
        out.append(" ".join(row))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
