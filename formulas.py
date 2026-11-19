import re

PERMITIDOS = re.compile(r"[0-9LA+\-*/(). ]+")

def avaliar(formula, L, A):
    if not PERMITIDOS.fullmatch(formula) or "**" in formula:
        raise ValueError(f"Fórmula inválida: {formula}")
    try: 
        return eval(formula, {"__builtins__": {}}, {"L": L, "A": A})
    except (SyntaxError, NameError, TypeError, ZeroDivisionError) as erro:
        raise ValueError(f"Fórmula inválida: {formula} ({erro})")