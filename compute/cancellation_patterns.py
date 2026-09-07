"""Exact local structure for the cancellation-descent investigation.

See docs/attacks/A10-cancellation-descent.md for the proofs and their scope.
No function here promotes a surviving label pattern to a global solution,
or excludes it without an assigned prime. No curve engine is imported.
"""
from fractions import Fraction

from compute.prime_column import column_certificate


ROLES = "ABCD"
LEADING_ROWS = {
    "A": ((0, -1, 1, 0), (0, 1, 0, 1)),
    "B": ((-1, 0, 1, 0), (-1, 0, 0, 1)),
    "C": ((1, 1, 0, 0), (-2, 0, 0, 1)),
    "D": ((-1, 1, 0, 0), (-2, 0, 1, 0)),
    "*": ((1, 1, -1, 0), (1, -1, 0, -1)),
}
LEADING_RAYS = {
    "A": (0, 1, 1, -1), "B": (1, 0, 1, 1),
    "C": (1, -1, 0, 2), "D": (1, 1, 2, 0),
}


def column_pattern(column, signs=(1, 1, 1, 1)):
    """Keep magnitudes AND offset signs; * means all four are maximal.

    A zero column belongs to a smaller prime support, not to the * stratum.
    The exact signed exponents are also recoverable from cand in the inventory.
    """
    if len(column) != 4 or len(signs) != 4 or any(s not in (-1, 1) for s in signs):
        raise ValueError("four exponents and four signs are required")
    column = tuple(int(e) for e in column)
    maximum = max(map(abs, column))
    if not maximum:
        return {"role": "zero", "maximum": 0}
    top = [i for i, e in enumerate(column) if abs(e) == maximum]
    if len(top) < 3:
        raise ValueError("column violates the prime-column lemma")
    missing = next((i for i in range(4) if i not in top), None)
    role = "*" if missing is None else ROLES[missing]
    gap = None if missing is None else maximum - abs(column[missing])
    return {
        "role": role, "maximum": maximum,
        "signed_ratios": [str(Fraction(s * e, maximum)) for e, s in zip(column, signs)],
        "gap": gap,
        "unit_congruence_power": 4 * maximum if gap is None else 2 * gap,
        "requires_2_square": role in ("C", "D"),
    }


def candidate_patterns(cand):
    if len(cand) != 8 or len({len(row) for row in cand[:4]}) != 1:
        raise ValueError("expected four equal-width labels followed by four signs")
    if column_certificate(cand[:4]) is not None:
        raise ValueError("candidate violates the prime-column lemma")
    return [column_pattern(c, cand[4:]) for c in zip(*cand[:4])]


def binomial_constraints(cand):
    """CP.4: exact unit-binomial data and necessary prime-height inequalities.

    At a deficient column j, W=prod_(k!=j) rho_k^(2*d_k) is congruent
    to lambda modulo pi_j^(2*gap). Its numerator minus lambda times
    its denominator is nonzero for distinct labels modulo sign.
    Consequently p_j^gap <= (1+abs(lambda))*prod_(k!=j) p_k^abs(d_k).
    Four-maximal columns still have trinomial constraints, omitted here.
    """
    patterns = candidate_patterns(cand)
    labels, signs = cand[:4], cand[4:]
    out = []
    for j, pattern in enumerate(patterns):
        if pattern["role"] not in "ABCD" or len(pattern["role"]) != 1:
            continue
        for row in LEADING_ROWS[pattern["role"]]:
            indices = [i for i, coefficient in enumerate(row) if coefficient]
            i = next(i for i in indices if abs(row[i]) == 1)
            other = next(k for k in indices if k != i)
            orient_i = 1 if labels[i][j] > 0 else -1
            orient_other = 1 if labels[other][j] > 0 else -1
            ds = [orient_other*y-orient_i*x for x, y in zip(labels[i], labels[other])]
            if ds[j] != 0 or not any(ds):
                raise ValueError("maximal labels must be distinct modulo sign")
            lam = -row[other] // row[i] * signs[other]*orient_other * signs[i]*orient_i
            out.append({"column": j, "role": pattern["role"], "pair": [i, other],
                        "gap": pattern["gap"], "half_exponents": ds, "lambda": lam,
                        "height_constant": 1+abs(lam), "height_powers": list(map(abs, ds))})
    return out


def height_direction(constraints, width, bound=4):
    """An exact positive recession direction for the binomial norm bounds.

    A witness proves these inequalities alone give no height cap, even
    after imposing positive lower bounds on the log-primes. It does not
    construct primes or solve any unit congruence. None means only that
    this bounded integer search found no witness.
    """
    from itertools import product
    for direction in product(range(1, bound+1), repeat=width):
        if all(c["gap"]*direction[c["column"]] <=
               sum(a*x for a, x in zip(c["height_powers"], direction)) for c in constraints):
            return list(direction)
    return None


def _add(a, b, scale=1):
    out = dict(a)
    for power, coefficient in b.items():
        out[power] = out.get(power, 0) + scale * coefficient
    return {p: c for p, c in out.items() if c}


def additive_witness(weights):
    """Construct exact Laurent y_X over Q with y_C=y_A+y_B, y_D=y_A-y_B.

    For each nonzero integer weight w_X, val(y_X)=-abs(w_X); for
    w_X=0, val(y_X)>=0. Solving z_X^2-y_X*z_X-1=0 then realizes ANY
    signs of the weights in an algebraic closure of Q((t)). See CP.1.
    Returns Laurent polynomials as {integer exponent: integer coefficient}.
    """
    pattern = column_pattern(weights)
    role, maximum = pattern["role"], pattern["maximum"]
    large = {-maximum: 1}
    if role in ("zero", "*"):
        u, v = large, {-maximum: 2}
    else:
        small = {-abs(weights[ROLES.index(role)]): 1}
        if role == "A":
            u, v = small, large
        elif role == "B":
            u, v = large, small
        elif role == "C":
            u, v = large, _add(small, large, -1)
        else:
            u, v = large, _add(large, small, -1)
    return u, v, _add(u, v), _add(u, v, -1)


def square_residue_parameters(role, p):
    """Normalized leading-square solutions at a supplied split prime p.

    Returns t=B/A for *; for a three-maximum role returns [1] if its
    fixed ray has square entries, else []. Zero at the deficient slot
    is permitted. This tests leading residues only, not full p-adic lifts.
    Caller supplies a prime p=1 mod 4.
    """
    if p < 5 or p % 4 != 1:
        raise ValueError("expected a split odd prime p=1 mod 4")
    squares = {x*x % p for x in range(1, p)}
    if role == "*":
        return [t for t in range(2, p-1)
                if all(x % p in squares for x in (t, 1+t, 1-t))]
    if role not in LEADING_RAYS:
        raise ValueError("expected a nonzero prime-column role")
    return [1] if all(x == 0 or x % p in squares for x in LEADING_RAYS[role]) else []
