from fractions import Fraction

def eng_to_float(val_str):
    try:
        if ' ' in str(val_str):
            parts = str(val_str).split(' ')
            return float(parts[0]) + float(Fraction(parts[1]))
        return float(Fraction(str(val_str)))
    except:
        return 0.0

def simplify_fraction_str(n, d):
    f = Fraction(n, d)
    return str(f.numerator) if f.denominator == 1 else f"{f.numerator}/{f.denominator}"

THICKNESS_FRACTIONS_LIMIT = [simplify_fraction_str(i, 16) for i in range(1, 17)]
THICKNESS_VALUES_LIMIT = {simplify_fraction_str(i, 16): i/16 for i in range(1, 17)}
THICKNESS_FRACTIONS_WIDE = [simplify_fraction_str(i, 16) for i in range(1, 113)]
THICKNESS_VALUES_WIDE = {simplify_fraction_str(i, 16): i/16 for i in range(1, 113)}

def format_eng_frac_no_unit(val):
    if val == 0.8125:
        return "13/16"
    if val == 0:
        return "0"
    res = Fraction(val).limit_denominator(64)
    if res.denominator == 1:
        return f"{res.numerator}"
    whole = res.numerator // res.denominator
    rem = res.numerator % res.denominator
    return f"{whole} {rem}/{res.denominator}" if whole > 0 else f"{rem}/{res.denominator}"

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
def format_gage_key(k: str) -> str:
    if isinstance(k, str) and k.startswith("g") and len(k) > 1 and k[1:].isdigit():
        return "g" + k[1:].translate(SUB)
    return k
