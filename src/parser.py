from lark import Lark, Transformer, v_args

calc_grammar = """
    ?start: expr

    ?expr: expr "or" term             -> or_op
         | term

    ?term: term "and" factor          -> and_op
         | factor

    ?factor: comparison
           | "not" factor             -> not_op
           | "(" expr ")"

    ?comparison: arithmetic COMPOP arithmetic  -> comparison
               | arithmetic

    ?arithmetic: arithmetic "+" term2   -> add
               | arithmetic "-" term2   -> sub
               | term2

    ?term2: term2 "*" factor2 -> mul
          | term2 "/" factor2 -> div
          | factor2

    ?factor2: NUMBER           -> number
            | BOOLEAN          -> bool
            | STRING           -> string
            | "-" factor2      -> neg
            | "(" arithmetic ")"

    COMPOP: "==" | "!=" | "<=" | ">=" | "<" | ">"

    BOOLEAN: "true" | "false"
    STRING: /"[^"]*"/

    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

@v_args(inline=True)
class CalcTransformer(Transformer):
    def number(self, n):
        return float(n)

    def bool(self, b):
        return b == "true"

    def string(self, s):
        return str(s[1:-1])  # Remove quotes clearly

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        return a / b

    def neg(self, a):
        return -a

    def comparison(self, a, op, b):
        op = str(op)
        if op == "==": return a == b
        if op == "!=": return a != b
        if op == "<":  return a < b
        if op == ">":  return a > b
        if op == "<=": return a <= b
        if op == ">=": return a >= b

    def and_op(self, a, b):
        return a and b

    def or_op(self, a, b):
        return a or b

    def not_op(self, a):
        return not a

parser = Lark(calc_grammar, parser='lalr', transformer=CalcTransformer())

def parse(text):
    return parser.parse(text)
