import sys

EPS = 1e-9
INF = 1e18

def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    m = int(tokens[0])
    n = int(tokens[1])

    # Tableau: (m + 1) rows, (n + m + 1) columns
    tab = [[0.0] * (n + m + 1) for _ in range(m + 1)]

    idx = 2
    # Objective function coefficients (row m)
    for j in range(n):
        c = float(tokens[idx])
        idx += 1
        tab[m][j] = -c

    # Constraints
    for i in range(m):
        for j in range(n):
            tab[i][j] = float(tokens[idx])
            idx += 1
        tab[i][n + i] = 1.0  # slack
        tab[i][n + m] = float(tokens[idx])  # rhs b_i
        idx += 1

    while True:
        # Entering variable: most negative in objective row
        enter_col = -1
        min_val = -EPS
        for j in range(n + m):
            if tab[m][j] < min_val:
                min_val = tab[m][j]
                enter_col = j

        if enter_col == -1:
            print("OPTIMAL")
            print(f"{tab[m][n + m]:.2f}")
            return

        # Leaving variable: min ratio test
        leave_row = -1
        min_ratio = INF
        for i in range(m):
            coeff = tab[i][enter_col]
            if coeff > EPS:
                ratio = tab[i][n + m] / coeff
                if ratio < min_ratio - EPS:
                    min_ratio = ratio
                    leave_row = i

        if leave_row == -1:
            print("UNBOUNDED")
            return

        # Pivot on (leave_row, enter_col)
        pivot_val = tab[leave_row][enter_col]
        leave_r = tab[leave_row]
        for j in range(n + m + 1):
            leave_r[j] /= pivot_val

        for i in range(m + 1):
            if i != leave_row:
                factor = tab[i][enter_col]
                if abs(factor) > EPS:
                    row_i = tab[i]
                    for j in range(n + m + 1):
                        row_i[j] -= factor * leave_r[j]

if __name__ == '__main__':
    main()
