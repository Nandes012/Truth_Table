import itertools
import re
# Fernandes Howard (0806022410014)
# Michael Vergo (0806022410007)

# Mapping from words/symbols to Python equivalents
replacements = {
    r"\band\b": " and ",
    r"\bor\b": " or ",
    r"\bnot\b": " not ",
    r"\bxor\b": " ^ ",
    r"\bequiv\b": " == ",      # handled later
    r"\bimplies\b": " -> ",    # temporary marker
    r"∧": " and ",
    r"∨": " or ",
    r"¬": " not ",
    r"⊕": " ^ ",
    r"⇔": " == ",              # handled later
    r"↔": " == ",
    r"⇒": " -> ",
    r"→": " -> ",
}

def normalize_expression(expr):
    # Step 1: basic replacements
    for pat, repl in replacements.items():
        expr = re.sub(pat, repl, expr)

    # Step 2: handle equivalence (a == b)
    expr = re.sub(r"(.+?)\s*==\s*(.+)", r"(\1) == (\2)", expr)

    # Step 3: handle implication (a -> b → (not a or b))
    expr = re.sub(r"(.+?)\s*->\s*(.+)", r"((not (\1)) or (\2))", expr)

    return expr

def evaluate_expression(expr, values):
    local_expr = expr
    for var, val in values.items():
        local_expr = re.sub(rf"\b{var}\b", str(val), local_expr)

    try:
        return eval(local_expr, {"__builtins__": None}, {})
    except Exception:
        return "ERR"

def main():
    print("Enter multiple logical expressions (p, q, r, A, B, etc.).")
    print("Allowed: and/or/not/xor/equiv/implies or ∧/∨/¬/⊕/⇔/↔/⇒/→")
    print("Type 'done' when finished.\n")

    raw_expressions = []
    variables = set()

    # Collect all expressions until "done"
    while True:
        expr = input(f"Expression {len(raw_expressions)+1}: ").strip()
        if expr.lower() == "done":
            break
        if expr:
            raw_expressions.append(expr)
            found_vars = re.findall(r"\b[A-Za-z]\b", expr)
            variables.update(found_vars)

    if not raw_expressions:
        print("No expressions entered.")
        return

    # Normalize all expressions
    expressions = [normalize_expression(expr) for expr in raw_expressions]
    variables = sorted(variables)

    # Build header
    header = "| " + " | ".join(f"{v:^5}" for v in variables) + " | " + " | ".join(f"{e:^25}" for e in raw_expressions) + " |"
    print("\nTruth Table:")
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    # Generate rows
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
        row += " | " + " | ".join(f"{r:^25}" for r in results) + " |"
        print(row)

    print("-" * len(header))

if __name__ == "__main__":
    main()
