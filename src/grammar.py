# src/grammar.py

calc_grammar = r"""
    // Entry point
    ?start: statement+

    // Statements
    ?statement: NAME "=" expr           -> assign_var
              | "print" expr            -> print_var
              | "if" expr block         -> if_stmt
              | "if" expr block "else" block -> if_else_stmt
              | "while" expr block      -> while_stmt
              | expr                    -> expr_stmt

    // Code block
    block: "{" statement+ "}"

    // Expression precedence
    ?expr: or_expr

    ?or_expr: and_expr
            | or_expr "or" and_expr    -> or_op

    ?and_expr: comparison
             | and_expr "and" comparison -> and_op

    ?comparison: sum
               | sum COMPOP sum         -> comparison

    // Arithmetic with precedence
    ?sum: product
        | sum "+" product               -> add
        | sum "-" product               -> sub

    ?product: factor
            | product "*" factor        -> mul
            | product "/" factor        -> div

    ?factor: "-" factor                 -> neg
           | "not" factor               -> not_op
           | atom

    ?atom: NUMBER                         -> number
         | STRING                         -> string
         | BOOLEAN                        -> bool_val  // New alias
         | NAME                           -> var
         | "input" "(" STRING ")"         -> input_expr
         | "(" expr ")"

    // Tokens (ensure BOOLEAN has higher priority than NAME)
    BOOLEAN.2: "true" | "false"       // Define BOOLEAN terminal again
    NAME.0: /[a-zA-Z_]\w*/
    STRING.1: /"[^"]*"/              // Give STRING a priority too
    NUMBER: /-?\d+(\.\d+)?/

    COMPOP: "==" | "!=" | "<=" | ">=" | "<" | ">"

    %ignore /\s+/
    %ignore /\/\/[^\n]*/
"""
