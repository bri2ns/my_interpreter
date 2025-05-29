from lark import Lark, Transformer, v_args

calc_grammar = """
    ?start: statement+

    ?statement: NAME "=" expr       -> assign_var
              | "print" expr        -> print_var
              | expr                -> expr_stmt

    ?expr: expr "or" term           -> or_op
         | term

    ?term: term "and" factor        -> and_op
         | factor

    ?factor: comparison
           | "not" factor           -> not_op
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
            | NAME             -> var
            | "-" factor2      -> neg
            | "(" arithmetic ")"

    COMPOP: "==" | "!=" | "<=" | ">=" | "<" | ">"
    BOOLEAN: "true" | "false"
    STRING: /"[^"]*"/
    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/

    %import common.NEWLINE
    %import common.WS
    %import common.NUMBER
    %ignore WS
    %ignore NEWLINE

"""

@v_args(inline=True)
class CalcTransformer(Transformer):
    def __init__(self):
        self.vars = {}

    def number(self, n):
        return float(n)

    def bool(self, b):
        return b == "true"

    def string(self, s):
        return str(s[1:-1])

    def var(self, name):
        return self.vars.get(str(name), None)

    def assign_var(self, name, value):
        self.vars[str(name)] = value

    def print_var(self, value):
        print(value)

    def expr_stmt(self, value):
        return value

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
    parser.parse(text)

