import itertools
import re
# Fernandes Howard (0806022410014)
# Michael Vergo (0806022410007)

# Safe logical operators
def logical_and(a, b): return a and b
def logical_or(a, b): return a or b
def logical_not(a): return not a
def logical_xor(a, b): return (a and not b) or (not a and b)

# Mapping from words/symbols to Python equivalents
replacements = {
    r"\band\b": " and ",
    r"\bor\b": " or ",
    r"\bnot\b": " not ",
    r"\bxor\b": " ^ ",
    r"∧": " and ",
    r"∨": " or ",
    r"¬": " not ",
    r"⊕": " ^ ",
}

def normalize_expression(expr):
    for pat, repl in replacements.items():
        expr = re.sub(pat, repl, expr)
    return expr

def evaluate_expression(expr, values):
    # Replace variables with True/False
    local_expr = expr
    for var, val in values.items():
        local_expr = re.sub(rf"\b{var}\b", str(val), local_expr)

    try:
        # Use Python's eval safely
        return eval(local_expr, {"__builtins__": None}, {})
    except Exception:
        return "ERR"

def main():
    expressions = []
    variables = set()

    print("Enter logical expressions (use variables like p, q, r).")
    print("Allowed operators: and/or/not/xor or ∧/∨/¬/⊕")
    print("Type 'done' when finished.\n")

    # Input expressions
    while True:
        expr = input(f"Expression {len(expressions)+1}: ")
        if expr.strip().lower() == "done":
            break
        expr = normalize_expression(expr)
        expressions.append(expr)

        # Find single-letter variables
        found_vars = re.findall(r"\b[a-z]\b", expr)
        variables.update(found_vars)

    variables = sorted(variables)

    # Build header
    header = "| " + " | ".join(f"{v:^5}" for v in variables) + " | " + " | ".join(f"{e:^20}" for e in expressions) + " |"
    print("\nTruth Table:")
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    # Generate truth table rows
    for combo in itertools.product([True, False], repeat=len(variables)):
        values = dict(zip(variables, combo))
        row = "| " + " | ".join("  T  " if values[v] else "  F  " for v in variables)

        results = []
        for expr in expressions:
            res = evaluate_expression(expr, values)
            if res is True:
                results.append("  T  ")
            elif res is False:
                results.append("  F  ")
            else:
                results.append(" ERR ")
        row += " | " + " | ".join(f"{r:^20}" for r in results) + " |"
        print(row)

    print("-" * len(header))

if __name__ == "__main__":
    main()
