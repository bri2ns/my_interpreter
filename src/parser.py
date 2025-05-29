from lark import Lark, Transformer, v_args

calc_grammar = """
    ?start: expr

    ?expr: expr "+" term   -> add
         | expr "-" term   -> sub
         | term

    ?term: term "*" factor -> mul
         | term "/" factor -> div
         | factor

    ?factor: NUMBER        -> number
           | "-" factor    -> neg
           | "(" expr ")"

    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

@v_args(inline=True)
class CalcTransformer(Transformer):
    def number(self, n):
        return float(n)

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

parser = Lark(calc_grammar, parser='lalr', transformer=CalcTransformer())

def parse(text):
    return parser.parse(text)
