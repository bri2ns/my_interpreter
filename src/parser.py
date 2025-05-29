# src/parser.py

from lark import Lark, Tree
import traceback

# Use relative imports if all these files are in the same 'src' package/directory
from grammar import calc_grammar
from interpreter import CalcTransformer

# Create a single transformer instance. Its state (self.vars) will persist
# across multiple calls to `parser_instance.parse()` if this module is imported once
# and `parse()` is called multiple times. This is suitable for running one script.
_persistent_transformer = CalcTransformer()
parser_instance = Lark(calc_grammar, parser='lalr', transformer=_persistent_transformer)

def parse(text_content):
    """
    Parses and executes the given text_content using the defined grammar and transformer.
    The transformer's state (e.g., variables) will persist across calls if this
    function is called multiple times within the same Python process/session,
    because it reuses the `_persistent_transformer` instance.

    If you need a fresh state for each call to `parse()`, you would either:
    1. Re-initialize the transformer: `_persistent_transformer.__init__()` here.
    2. Create a new Lark parser and transformer instance inside this function (less efficient).
    """
    try:
        # If you wanted to reset variables for every independent script run from main.py
        # and main.py calls parse() for each script:
        # _persistent_transformer.vars.clear() # or _persistent_transformer.__init__()

        parsed_result = parser_instance.parse(text_content) # Use the shared parser instance
        print("[INFO] Input parsed. Executing statements...")

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
        # traceback.print_exc() # Uncomment for full trace if needed