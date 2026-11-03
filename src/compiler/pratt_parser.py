import sys

class ASTNode:
    def __init__(self, op="", val=0, left=None, right=None):
        self.op = op
        self.val = val
        self.left = left
        self.right = right

    def to_sexpr(self):
        if not self.op:
            return str(self.val)
        if not self.right:
            return f"({self.op} {self.left.to_sexpr()})"
        return f"({self.op} {self.left.to_sexpr()} {self.right.to_sexpr()})"

    def eval(self):
        if not self.op:
            return self.val
        if not self.right:
            if self.op == "-":
                return -self.left.eval()
            return self.left.eval()
        l = self.left.eval()
        r = self.right.eval()
        if self.op == "+":
            return l + r
        if self.op == "-":
            return l - r
        if self.op == "*":
            return l * r
        if self.op == "/":
            if r == 0:
                return 0
            sign = -1 if (l < 0) ^ (r < 0) else 1
            return sign * (abs(l) // abs(r))
        if self.op == "^":
            res = 1
            for _ in range(r):
                res *= l
            return res
        return 0

class Lexer:
    def __init__(self, src):
        self.src = src
        self.pos = 0

    def next_token(self):
        while self.pos < len(self.src) and self.src[self.pos].isspace():
            self.pos += 1
        if self.pos >= len(self.src):
            return ("EOF", 0)
        c = self.src[self.pos]
        if c.isdigit():
            val = 0
            while self.pos < len(self.src) and self.src[self.pos].isdigit():
                val = val * 10 + int(self.src[self.pos])
                self.pos += 1
            return ("NUMBER", val)
        self.pos += 1
        if c in "+-*/^()":
            return (c, 0)
        return ("EOF", 0)

class PrattParser:
    def __init__(self, s):
        self.lexer = Lexer(s)
        self.advance()

    def advance(self):
        self.curr = self.lexer.next_token()

    def infix_binding_power(self, op):
        if op in ("+", "-"):
            return (10, 11)
        if op in ("*", "/"):
            return (20, 21)
        if op == "^":
            return (31, 30)
        return (-1, -1)

    def parse_expression(self, min_bp=0):
        # Prefix
        tok_type, val = self.curr
        if tok_type == "NUMBER":
            lhs = ASTNode(val=val)
            self.advance()
        elif tok_type == "-":
            self.advance()
            rhs = self.parse_expression(40)
            if rhs is None:
                return None
            lhs = ASTNode(op="-", left=rhs)
        elif tok_type == "(":
            self.advance()
            lhs = self.parse_expression(0)
            if self.curr[0] == ")":
                self.advance()
        else:
            return None

        # Infix
        while True:
            l_bp, r_bp = self.infix_binding_power(self.curr[0])
            if l_bp < min_bp:
                break

            op_str = self.curr[0]
            self.advance()

            rhs = self.parse_expression(r_bp)
            if rhs is None:
                return None
            lhs = ASTNode(op=op_str, left=lhs, right=rhs)

        return lhs

def main():
    lines = sys.stdin.read().splitlines()
    if not lines:
        return
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    if idx >= len(lines):
        return
    try:
        num_exprs = int(lines[idx].strip())
    except ValueError:
        return
    idx += 1

    out = []
    for _ in range(num_exprs):
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        if idx >= len(lines):
            break
        line = lines[idx]
        idx += 1
        parser = PrattParser(line)
        ast = parser.parse_expression()
        if ast:
            out.append(f"{ast.to_sexpr()} = {ast.eval()}")
        else:
            out.append("PARSE_ERROR")

    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    main()
