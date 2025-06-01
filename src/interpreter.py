from lark import Transformer, v_args

@v_args(inline=True)
class CalcTransformer(Transformer):
    def __init__(self):
        self.vars = {}

    def number(self, n_token): return lambda: float(n_token)
    def bool(self, b_token):
        return lambda: str(b_token) == "true"
    def string(self, s_token): return lambda: str(s_token[1:-1])
    def var(self, name_token):
        name_str = str(name_token)
        return lambda: self.vars[name_str] if name_str in self.vars else self._undefined(name_str)

    def _undefined(self, name):
        raise RuntimeError(f"Undefined variable: '{name}'")

    def assign_var(self, name_token, value_lambda):
        name_str = str(name_token)
        return lambda: self._assign(name_str, value_lambda)

    def _assign(self, name, value_lambda):
        val = value_lambda()
        self.vars[name] = val
        return val

    def print_var(self, value_lambda):
        return lambda: print(f"[OUTPUT] {value_lambda()}")

    def expr_stmt(self, value_lambda):
        return lambda: print(f"[OUTPUT] {value_lambda()}")

    def _execute_add(self, val_a, val_b):
        if isinstance(val_a, str) or isinstance(val_b, str):
            return str(val_a) + str(val_b)
        elif isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
            return val_a + val_b
        else:
            return self._runtime_error(f"Unsupported operand types for +: {type(val_a).__name__} and {type(val_b).__name__}")

    def add(self, a_lambda, b_lambda):
        return lambda: self._execute_add(a_lambda(), b_lambda())

    def _checked_sub(self, val_a, val_b):
        if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
            return val_a - val_b
        else:
            return self._runtime_error(f"Unsupported operand types for -: {type(val_a).__name__} and {type(val_b).__name__}")

    def sub(self, a_lambda, b_lambda):
        return lambda: self._checked_sub(a_lambda(), b_lambda())


    def _checked_mul(self, val_a, val_b):
        if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
            return val_a * val_b
        else:
            return self._runtime_error(f"Unsupported operand types for *: {type(val_a).__name__} and {type(val_b).__name__}")

    def mul(self, a_lambda, b_lambda):
        return lambda: self._checked_mul(a_lambda(), b_lambda())

    def _checked_div(self, val_a, val_b):
        if not (isinstance(val_a, (int, float)) and isinstance(val_b, (int, float))):
            return self._runtime_error(f"Unsupported operand types for /: {type(val_a).__name__} and {type(val_b).__name__}")
        if val_b == 0:
            return self._runtime_error("Division by zero")
        return val_a / val_b

    def div(self, a_lambda, b_lambda):
        return lambda: self._checked_div(a_lambda(), b_lambda())

    def _execute_neg(self, val_a):
        if isinstance(val_a, bool): # CHECK FOR BOOLEAN FIRST!
            result = not val_a
            return result
        elif isinstance(val_a, (int, float)): # Then check for int/float
            result = -val_a
            return result
        else:
            return self._runtime_error(f"Unsupported type for negation/not: {type(val_a).__name__}")

    def neg(self, a_lambda): # For unary numeric negation
        return lambda: self._execute_neg(a_lambda())

    def _runtime_error(self, message):
        raise RuntimeError(message)

    def _execute_comparison(self, val_a, op_str, val_b):
        if op_str == "==":
            return val_a == val_b
        if op_str == "!=":
            return val_a != val_b

        if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
            pass
        elif isinstance(val_a, str) and isinstance(val_b, str):
            pass
        elif isinstance(val_a, bool) and isinstance(val_b, bool):
             pass
        else:
            return self._runtime_error(f"Cannot perform ordered comparison ({op_str}) between {type(val_a).__name__} and {type(val_b).__name__}")

        if op_str == "<": return val_a < val_b
        if op_str == ">": return val_a > val_b
        if op_str == "<=": return val_a <= val_b
        if op_str == ">=": return val_a >= val_b
        
        return self._runtime_error(f"Unknown comparison operator: {op_str}")

    def comparison(self, a_lambda, op_token, b_lambda):
        op_str = str(op_token)
        return lambda: self._execute_comparison(a_lambda(), op_str, b_lambda())

    def and_op(self, a_lambda, b_lambda): return lambda: a_lambda() and b_lambda()
    def or_op(self, a_lambda, b_lambda): return lambda: a_lambda() or b_lambda()
    
    def not_op(self, a_lambda):
        return lambda: self._execute_neg(a_lambda())

    def input_expr(self, string_token):
        prompt = str(string_token)[1:-1]
        return lambda: input(prompt)

    def block(self, *statements_lambdas):
        return list(statements_lambdas)

    def if_stmt(self, condition_lambda, block_content_list):
        def _if_executor():
            cond_val = condition_lambda()
            if cond_val:
                for stmt_lambda in block_content_list:
                    stmt_lambda()
            return None
        return _if_executor

    def if_else_stmt(self, condition_lambda, block_true_list, block_false_list):
        def _if_else_executor():
            cond_val = condition_lambda()
            if cond_val:
                for stmt_lambda in block_true_list:
                    stmt_lambda()
            else:
                for stmt_lambda in block_false_list:
                    stmt_lambda()
        return _if_else_executor

    def while_stmt(self, condition_lambda, block_content_list):
        def loop():
            while True:
                cond_val = condition_lambda()
                if not cond_val:
                    break
                for stmt_lambda in block_content_list:
                    stmt_lambda()
        return loop