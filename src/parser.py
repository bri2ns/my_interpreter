
from lark import Lark, Tree
import traceback

from grammar import calc_grammar
from interpreter import CalcTransformer

_persistent_transformer = CalcTransformer()
parser_instance = Lark(calc_grammar, parser='lalr', transformer=_persistent_transformer)

def parse(text_content):

    try:
        parsed_result = parser_instance.parse(text_content)

        statements_to_execute = []

        if isinstance(parsed_result, Tree):
            statements_to_execute = parsed_result.children
        elif isinstance(parsed_result, list):
            statements_to_execute = parsed_result
        elif callable(parsed_result):
            statements_to_execute = [parsed_result]
        elif parsed_result is None:
            print("[INFO] Parse result is None. No statements to execute.")
            return
        else:
            print(f"[ERROR] Unexpected type from parser.parse(): {type(parsed_result)}. Value: {parsed_result}")
            return

        if not statements_to_execute:
            if parsed_result is not None:
                 print(f"[INFO] No executable statements derived from parsed_result (type: {type(parsed_result).__name__}).")
            else:
                print("[INFO] No statements to execute.")
            return

        for i, stmt_lambda in enumerate(statements_to_execute):
            if callable(stmt_lambda):
                try:
                    stmt_lambda()
                except RuntimeError as e_stmt:
                    print(f"[RUNTIME ERROR] {e_stmt}")
                except Exception as e_stmt:
                    print(f"[UNEXPECTED ERROR] {e_stmt}")
                    traceback.print_exc()
            else:
                print(f"[ERROR] Internal: Statement {i + 1} is not callable: {stmt_lambda} (type: {type(stmt_lambda).__name__})")

    except Exception as e_parse:
        print(f"[PARSING ERROR] {e_parse}")
        # traceback.print_exc()