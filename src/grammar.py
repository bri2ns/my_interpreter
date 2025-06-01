# src/grammar.py

calc_grammar = """
    ?start: statement+

    ?statement: NAME "=" expr            -> assign_var
              | "print" expr            -> print_var
              | "if" expr block         -> if_stmt
              | "if" expr block "else" block -> if_else_stmt
              | "while" expr block      -> while_stmt
            //  | "input" "(" STRING ")"  -> input_expr   // REMOVED from here
              | expr                    -> expr_stmt

    block: "{" statement+ "}"

    expr: expr "or" term             -> or_op
         | term

    term: term "and" factor          -> and_op
         | factor

    factor: comparison
           | "not" factor            -> not_op
           | "(" expr ")"

    comparison: arithmetic COMPOP arithmetic -> comparison
               | arithmetic

    arithmetic: arithmetic "+" term2  -> add
               | arithmetic "-" term2  -> sub
               | term2

    term2: term2 "*" factor2 -> mul
          | term2 "/" factor2 -> div
          | factor2

    factor2: NUMBER              -> number
            | BOOLEAN             -> bool
            | STRING              -> string
            | NAME                -> var
            | "input" "(" STRING ")"  -> input_expr   // ADDED here
            | "-" factor2         -> neg
            | "(" arithmetic ")"

    COMPOP: "==" | "!=" | "<=" | ">=" | "<" | ">"

    // --- Terminal Priorities ---
    // Higher number means higher priority.
    // This helps ensure "true" and "false" are seen as BOOLEANs, not NAMEs.
    BOOLEAN.2: "true" | "false"
    STRING.1: /"[^"]*"/
    NAME.0: /[a-zA-Z_][a-zA-Z0-9_]*/

    %import common.NUMBER
    %import common.NEWLINE
    %import common.WS
    %ignore WS
    %ignore NEWLINE
"""