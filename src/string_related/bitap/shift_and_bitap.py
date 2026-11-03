import sys

def shift_and_bitap_k_mismatch(k, pattern, text):
    m = len(pattern)
    n = len(text)
    if m == 0 or m > n:
        return []

    mask_all = (1 << m) - 1
    char_mask = [0] * 26
    for i, ch in enumerate(pattern):
        c = ord(ch) - ord('a')
        char_mask[c] |= (1 << i)

    r = [0] * (k + 1)
    accept_bit = 1 << (m - 1)
    matches = []

    for j, ch in enumerate(text):
        c = ord(ch) - ord('a')
        bc = char_mask[c]
        prev_shifted = ((r[0] << 1) | 1) & mask_all
        r[0] = prev_shifted & bc
        for d in range(1, k + 1):
            cur_shifted = ((r[d] << 1) | 1) & mask_all
            r[d] = (cur_shifted & bc) | prev_shifted
            prev_shifted = cur_shifted
        if j + 1 >= m and (r[k] & accept_bit) != 0:
            matches.append(j + 1 - m)

    return matches

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    it = iter(tokens)
    q = int(next(it))
    out = []

    for _ in range(q):
        k = int(next(it))
        pattern = next(it)
        text = next(it)
        matches = shift_and_bitap_k_mismatch(k, pattern, text)
        if not matches:
            out.append("-1")
        else:
            out.append(" ".join(str(x) for x in matches))

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
