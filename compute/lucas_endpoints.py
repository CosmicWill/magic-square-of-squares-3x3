"""Front A step 2 (ROADMAP R.6-A): the mechanical ENDPOINT EXTRACTOR for
the (a,b) ladder -- what the hand-trees of A3.8/A3.9/A3.10 did by hand,
done once for every pattern.

Setting (two split primes; the engine's conventions).  A pattern is a
signed relation  sum_i c_i Im(sigma^{j_i} tau^{k_i}) = 0  and its
cleared form is  sum_i c_i p^{2(J-|j_i|)} q^{2(K-|k_i|)} Im(l^{2j_i} w^{2k_i})
with l = pi^2 = c1 + i s1, w = rho^2 = c2 + i s2, negative exponents
meaning conjugates.  Three facts drive the extractor:

  (1) COLLAPSE.  For any two terms the sum-to-product identity holds
      EXACTLY with the cleared weights:  the pair collapses to
      +-2 p^{2a} q^{2b} Trig1(D) Trig2(M)  with D, M the half-difference /
      half-sum monomials (Trig in {Re, Im}).  We do not trust the sign
      conventions: every collapse is found by exact polynomial identity
      over Z[c1,s1,c2,s2].
  (2) UNITS.  A trig-monomial involving l (x != 0) is a p-unit and one
      involving w is a q-unit (pi divides one of the two conjugate
      products, never both).  Only a PURE-w monomial can absorb a power
      of p, only a pure-l one a power of q.
  (3) LEVER.  After collapsing the pair of minimal weight at a prime P,
      the third term's surplus weight P^e must divide the product; by
      (2) it must land on a pure factor of the other prime, else the
      pattern is DEAD.  What remains is the ENDPOINT:
          P^e | Trig(pure monomial)   and   the residual product equation,
      which after absorption is a coincidence between trig-monomials of
      the two primes -- the Lucas-coincidence family (the rigidity lemma
      is  Re(w^4) = +-p^2 Re(l^2)).
"""
from __future__ import annotations

from compute.two_prime_additive import (gauss_pow, p4add, p4mul, ELL, W,
                                        P2, Q2)


def _neg(P):
    return {k: -v for k, v in P.items()}


def trig(kind, x, y):
    """Re/Im of l^x w^y in Z[c1,s1,c2,s2]; negative exponents = conjugates."""
    Rl, Il = gauss_pow(*ELL, abs(x))
    if x < 0:
        Il = _neg(Il)
    Rw, Iw = gauss_pow(*W, abs(y))
    if y < 0:
        Iw = _neg(Iw)
    R = p4add(p4mul(Rl, Rw), p4mul(Il, Iw), -1)
    I = p4add(p4mul(Rl, Iw), p4mul(Il, Rw))
    return R if kind == "Re" else I


def scale(P, c):
    return {k: c * v for k, v in P.items()} if c != 1 else dict(P)


def times_pq(P, a, b):
    for _ in range(a):
        P = p4mul(P, P2)
    for _ in range(b):
        P = p4mul(P, Q2)
    return P


def cleared_terms(pattern):
    """[(c, wp, wq, (2j, 2k), poly)] with poly = c p^{2wp} q^{2wq} Im(l^{2j} w^{2k})."""
    J = max(abs(j) for (j, k), c in pattern)
    K = max(abs(k) for (j, k), c in pattern)
    out = []
    for (j, k), c in pattern:
        T = trig("Im", 2 * j, 2 * k)
        wp, wq = J - abs(j), K - abs(k)
        out.append((c, wp, wq, (2 * j, 2 * k), scale(times_pq(T, wp, wq), c)))
    return out


def deg_pq(P):
    """(degree in (c1,s1), degree in (c2,s2)) of a homogeneous-per-prime poly."""
    return (max(a + b for a, b, c, d in P), max(c + d for a, b, c, d in P))


def find_collapse(ta, tb):
    """Exact identity  ta.poly + tb.poly == s * 2 * p^{2a} q^{2b} Trig1(D) Trig2(M)
    for D, M in the natural half-sum/half-difference candidates.  Returns
    (s, a, b, kind1, D, kind2, M) or None."""
    ca, wpa, wqa, ea, Pa = ta
    cb, wpb, wqb, eb, Pb = tb
    S = p4add(Pa, Pb)
    if not S:
        return None
    dS = deg_pq(S)
    (x1, y1), (x2, y2) = ea, eb
    cands = set()
    for sx in (1, -1):
        for sy in (1, -1):
            # half-sum and half-difference with sign variants (conjugation freedom)
            hs = ((x1 + sx * x2) // 2, (y1 + sy * y2) // 2)
            hd = ((x1 - sx * x2) // 2, (y1 - sy * y2) // 2)
            if (x1 + sx * x2) % 2 or (y1 + sy * y2) % 2:
                continue
            for D, M in ((hd, hs), (hs, hd)):
                for D2 in (D, (-D[0], D[1]), (D[0], -D[1]), (-D[0], -D[1])):
                    for M2 in (M, (-M[0], M[1]), (M[0], -M[1]), (-M[0], -M[1])):
                        cands.add((D2, M2))
    for D, M in cands:
        for k1 in ("Re", "Im"):
            for k2 in ("Re", "Im"):
                T = p4mul(trig(k1, *D), trig(k2, *M))
                T = scale(T, 2)
                if not T:
                    continue
                dT = deg_pq(T)
                a2, b2 = dS[0] - dT[0], dS[1] - dT[1]
                if a2 < 0 or b2 < 0 or a2 % 2 or b2 % 2:
                    continue
                T = times_pq(T, a2 // 2, b2 // 2)
                if T == S:
                    return (1, a2 // 2, b2 // 2, k1, D, k2, M)
                if _neg(T) == S:
                    return (-1, a2 // 2, b2 // 2, k1, D, k2, M)
    return None


def is_pure_w(m):
    return m[0] == 0 and m[1] != 0


def is_pure_l(m):
    return m[1] == 0 and m[0] != 0


def extract(pattern):
    """The endpoint of one OPEN pattern.  Returns a dict with
    'status' in {'DEAD-no-pure-factor', 'ENDPOINT', 'NO-LEVER', 'NO-COLLAPSE'}."""
    terms = cleared_terms(pattern)
    n = len(terms)
    if n != 3:
        return {"status": "NOT-3-TERMS"}
    results = []
    for prime in ("p", "q"):
        wi = 1 if prime == "p" else 2
        ws = [t[wi] for t in terms]
        m = min(ws)
        low = [i for i in range(3) if ws[i] == m]
        if len(low) != 2:
            continue                      # no lever at this prime (all equal or single min: pruned)
        a, b = low
        c = ({0, 1, 2} - {a, b}).pop()
        col = find_collapse(terms[a], terms[b])
        if col is None:
            results.append({"prime": prime, "status": "NO-COLLAPSE"})
            continue
        s, ap, bq, k1, D, k2, M = col
        # relation:  s*2*p^{2ap} q^{2bq} T1(D) T2(M) = -term_c
        cc, wpc, wqc, ec, Pc = terms[c]
        ep, eq = wpc - ap, wqc - bq          # surplus of the third term (may be negative)
        # which side must absorb which power
        absorb = {}
        dead = False
        for P, e, pure in (("p", ep, is_pure_w), ("q", eq, is_pure_l)):
            if e > 0:
                fac = [("D", D, k1) if pure(D) else None, ("M", M, k2) if pure(M) else None]
                fac = [f for f in fac if f]
                if not fac:
                    dead = True
                absorb[P] = ("product", 2 * e, fac)
            elif e < 0:
                if not pure(ec):
                    dead = True
                absorb[P] = ("third", -2 * e, ("C", ec, "Im"))
        results.append({"prime": prime, "status": "DEAD-no-pure-factor" if dead else "ENDPOINT",
                        "pair": (a, b), "third": c, "sign": s, "kinds": (k1, k2), "D": D, "M": M,
                        "C": ec, "coeff_c": cc, "absorb": absorb})
    if not results:
        return {"status": "NO-LEVER"}
    if any(r["status"] == "DEAD-no-pure-factor" for r in results):
        return {"status": "DEAD-no-pure-factor", "detail": results}
    if all(r["status"] == "NO-COLLAPSE" for r in results):
        return {"status": "NO-COLLAPSE", "detail": results}
    return {"status": "ENDPOINT", "detail": [r for r in results if r["status"] == "ENDPOINT"]}


# ---------------------------------------------------------------- the chase
#
# Lucas values: U_y = Re(w^y), V_y = Im(w^y), C_x = Re(l^x), S_x = Im(l^x)
# (y, x >= 1).  Facts used by the chase, all classical for primitive
# Gaussian powers:  gcd(U_y, V_y) = 1 = gcd(C_x, S_x);  U_y, C_x odd and
# V_y, S_x even;  U_y, V_y are p-units and C_x, S_x are q-units;
# U_{2y} = U_y^2 - V_y^2, V_{2y} = 2 U_y V_y (same for C, S).
#
# An endpoint  s*2*T1(D)*T2(M) = -c * p^{2ep} q^{2eq} * Im(C)  is turned
# into a polynomial identity in the Lucas symbols of ONE w-exponent and
# ONE l-exponent (after double-angle reduction), verified as an exact
# identity in Z[c1,s1,c2,s2].  Then the chase collects the symbol shared
# by both sides into a product form and applies the coprimality rules.

import sympy as _sp

_c1, _s1, _c2, _s2 = _sp.symbols("c1 s1 c2 s2")
_P, _Q = _sp.symbols("p q", positive=True)


def _poly_expr(P):
    return sum(v * _c1**a * _s1**b * _c2**c * _s2**d for (a, b, c, d), v in P.items())


def lucas_expr(kind, x, y):
    """Trig(l^x w^y) written in the symbols U_|y|, V_|y|, C_|x|, S_|x|
    (conjugation = sign flip of the Im part), as a sympy expression."""
    Ux, Vx = _sp.Symbol(f"C{abs(x)}"), _sp.Symbol(f"S{abs(x)}")
    Uy, Vy = _sp.Symbol(f"U{abs(y)}"), _sp.Symbol(f"V{abs(y)}")
    if x == 0:
        Ux, Vx = _sp.Integer(1), _sp.Integer(0)
    if y == 0:
        Uy, Vy = _sp.Integer(1), _sp.Integer(0)
    if x < 0:
        Vx = -Vx
    if y < 0:
        Vy = -Vy
    re = Ux * Uy - Vx * Vy
    im = Ux * Vy + Vx * Uy
    return re if kind == "Re" else im


def lucas_value(sym):
    """The polynomial (as sympy expr in c1,s1,c2,s2) of a Lucas symbol."""
    name, n = sym.name[0], int(sym.name[1:])
    kind = "Re" if name in "UC" else "Im"
    if name in "UV":
        return _poly_expr(trig(kind, 0, n))
    return _poly_expr(trig(kind, n, 0))


def _multiple_angle(Cg, Sg, k):
    """(Re, Im) of (Cg + i Sg)^k as polynomials in the symbols Cg, Sg."""
    R, I = _sp.Integer(1), _sp.Integer(0)
    for _ in range(k):
        R, I = _sp.expand(R * Cg - I * Sg), _sp.expand(R * Sg + I * Cg)
    return R, I


def reduce_to_base(expr, y0, x0):
    """Rewrite every w-side symbol U_n, V_n through the base exponent y0
    (n a multiple of y0) by the multiple-angle polynomials of
    (U_{y0} + i V_{y0})^{n/y0}, and every l-side symbol C_n, S_n through
    x0 likewise.  Callers pass y0 = gcd of the w-exponents present and
    x0 = gcd of the l-exponents present, so every symbol reduces."""
    from math import gcd
    subs = {}
    for sy in expr.free_symbols:
        nm = str(sy)
        if nm[0] not in "UVCS":
            continue
        n = int(nm[1:])
        base = y0 if nm[0] in "UV" else x0
        if base == 0 or n == base or n % base:
            continue
        if nm[0] in "UV":
            R, I = _multiple_angle(_sp.Symbol(f"U{base}"), _sp.Symbol(f"V{base}"), n // base)
            subs[sy] = R if nm[0] == "U" else I
        else:
            R, I = _multiple_angle(_sp.Symbol(f"C{base}"), _sp.Symbol(f"S{base}"), n // base)
            subs[sy] = R if nm[0] == "C" else I
    return _sp.expand(expr.subs(subs))


def endpoint_identity(pattern, detail):
    """The endpoint as  LHS - RHS = 0  in Lucas symbols, plus the base
    exponents (y0, x0) and the verification that the identity holds
    exactly in Z[c1,s1,c2,s2].  Returns (expr, y0, x0, ep, eq, ok)."""
    terms = cleared_terms(pattern)
    a, b = detail["pair"]
    c = detail["third"]
    s = detail["sign"]
    k1, k2 = detail["kinds"]
    D, M, C = detail["D"], detail["M"], detail["C"]
    # weights of the collapsed pair (min) and of the third term
    ap, bq = min(terms[a][1], terms[b][1]), min(terms[a][2], terms[b][2])
    cc, wpc, wqc = terms[c][0], terms[c][1], terms[c][2]
    ep, eq = wpc - ap, wqc - bq
    lhs = s * 2 * lucas_expr(k1, *D) * lucas_expr(k2, *M)
    rhs = -cc * lucas_expr("Im", *C)
    if ep >= 0:
        rhs = rhs * _P**(2 * ep)
    else:
        lhs = lhs * _P**(-2 * ep)
    if eq >= 0:
        rhs = rhs * _Q**(2 * eq)
    else:
        lhs = lhs * _Q**(-2 * eq)
    expr = _sp.expand(lhs - rhs)
    # base exponents: the gcd of the w- and of the l-exponents present
    from math import gcd
    from functools import reduce
    ys = {int(str(sy)[1:]) for sy in expr.free_symbols if str(sy)[0] in "UV"}
    xs = {int(str(sy)[1:]) for sy in expr.free_symbols if str(sy)[0] in "CS"}
    y0 = reduce(gcd, ys) if ys else 0
    x0 = reduce(gcd, xs) if xs else 0
    red = reduce_to_base(expr, y0, x0) if (y0 or x0) else expr
    # verify exactly: the symbol expression is the EQUATION (not an
    # identity); substituting the Lucas polynomials and p^2 = c1^2+s1^2,
    # q^2 = c2^2+s2^2 it must reproduce the cleared relation divided by
    # the common weight p^{2 mp} q^{2 mq}.
    check = red
    for sy in list(red.free_symbols):
        nm = str(sy)
        if nm[0] in "UVCS":
            check = check.subs(sy, lucas_value(sy))
    check = _sp.expand(check.subs({_P**2: _c1**2 + _s1**2, _Q**2: _c2**2 + _s2**2}))
    mp, mq = min(t[1] for t in terms), min(t[2] for t in terms)
    rel = _sp.Integer(0)
    for t in terms:
        rel += _poly_expr(t[4])
    lhs_full = _sp.expand(check * (_c1**2 + _s1**2)**mp * (_c2**2 + _s2**2)**mq)
    ok = _sp.expand(lhs_full - rel) == 0
    return red, y0, x0, ep, eq, ok


def _side_of(sym):
    n = str(sym)
    return "w" if n[0] in "UV" else ("l" if n[0] in "CS" else n)


def _coprime(A, B, facts):
    """Known-coprime oracle for atoms (symbols, p, q, or binomials)."""
    if A == B:
        return False
    a, b = str(A), str(B)
    if (A, B) in facts or (B, A) in facts:
        return True
    # Pythagorean legs of the same power are coprime
    if a[0] in "UV" and b[0] in "UV" and a[1:] == b[1:] and a[0] != b[0]:
        return True
    if a[0] in "CS" and b[0] in "CS" and a[1:] == b[1:] and a[0] != b[0]:
        return True
    # cross-exponent Lucas rules on one side: with n | m and m/n = 2^t
    # (t >= 1), C_m = C_n^2 - S_n^2 (doubling) is coprime to both C_n
    # and S_n (C_m = -S_n^2 mod C_n, = C_n^2 mod S_n, legs coprime);
    # and U/V likewise.  (S_m is NOT coprime to S_n: S_n | S_m.)
    def _is_lucas(sym, s):
        return getattr(sym, "is_Symbol", False) and len(s) >= 2 and s[0] in "UVCS" and s[1:].isdigit()
    if _is_lucas(A, a) and _is_lucas(B, b):
        for re_, im_ in (("C", "S"), ("U", "V")):
            if a[0] in (re_, im_) and b[0] in (re_, im_):
                na, nb = int(a[1:]), int(b[1:])
                if na != nb:
                    lo, hi = (na, nb) if na < nb else (nb, na)
                    big = a if na > nb else b
                    if hi % lo == 0 and (hi // lo) & (hi // lo - 1) == 0 and big[0] == re_:
                        return True                # C_{2^t n} coprime to C_n and S_n
    # unit-ness (STRUCTURAL): l-side values C_x, S_x are p-units (pi divides
    # one conjugate power, never both); w-side values U_y, V_y are q-units.
    # A p-power dividing a w-side value is CONTENT (a lever), never assumed.
    if (a == "p" and b[0] in "CS") or (b == "p" and a[0] in "CS"):
        return True
    if (a == "q" and b[0] in "UV") or (b == "q" and a[0] in "UV"):
        return True
    if {a, b} == {"p", "q"}:
        return True
    return False


def _atoms(factors):
    out = {}
    for f in factors:
        if f.is_number:
            out["const"] = out.get("const", 1) * int(f)
            continue
        base, e = (f.base, int(f.exp)) if f.is_Pow else (f, 1)
        out[base] = out.get(base, 0) + e
    return out


def _binomial_facts(binom, facts):
    """Coprimality facts for a polynomial atom:  gcd(aX + bY, X) =
    gcd(bY, X); and mod a prime P dividing one of two terms it is the
    other term."""
    for s in binom.free_symbols:
        rest = _sp.expand(binom.subs(s, 0))
        if rest == 0:
            continue
        rat = _atoms(_sp.Mul.make_args(_sp.factor(rest)))
        ok = True
        for a in rat:
            if a == "const":
                if abs(rat[a]) % 2 == 0 and str(s)[0] not in "UC":
                    ok = False              # only U, C are known odd
                continue
            if not _coprime(a, s, facts):
                ok = False
        if ok:
            facts.add((binom, s))
    for P_ in (_P, _Q):
        if is_unit_at(binom, P_):
            facts.add((binom, P_))


_W, _WB = _sp.symbols("W WB")            # w and wbar as independent variables


def to_gaussian(expr):
    """Lucas symbols of BOTH sides -> polynomial in L, LB (l, lbar) and
    W, WB (w, wbar), with p^2 = L LB and q^2 = W WB."""
    subs = {}
    for s in expr.free_symbols:
        nm = str(s)
        if nm[0] in "UVCS" and nm[1:].isdigit():
            n = int(nm[1:])
            A, B = (_L, _LB) if nm[0] in "CS" else (_W, _WB)
            subs[s] = (A**n + B**n) / 2 if nm[0] in "CU" else (A**n - B**n) / (2 * _sp.I)
    e = expr.subs(subs)
    e = e.subs({_P**2: _L * _LB, _Q**2: _W * _WB})
    return _sp.expand(e)


def is_unit_at(G, P_):
    """STRUCTURAL unit test: G (Lucas symbols, p, q) is a P-unit when its
    reduction modulo the Gaussian prime over P -- l -> 0 for p (pi | l,
    pi never divides lbar, w, wbar), w -> 0 for q -- is a single monomial
    c * lbar^a w^b wbar^c ... with c a nonzero rational whose numerator is
    prime to P (constants in play are tiny; P >= 5)."""
    g = to_gaussian(G)
    g0 = _sp.expand(g.subs(_L if P_ == _P else _W, 0))
    if g0 == 0:
        return False
    terms = _sp.Add.make_args(g0)
    if len(terms) != 1:
        return False
    coeff, _ = terms[0].as_coeff_Mul()
    coeff = _sp.nsimplify(coeff)
    n_ = _sp.expand(coeff * _sp.conjugate(coeff))          # Gaussian norm, rational
    if not n_.is_rational or n_ == 0:
        return False
    num = abs(_sp.Rational(n_).p)
    return all(num % pr for pr in (5, 7, 11, 13, 17, 19, 23))


def _closure(Lat, Rat, facts):
    """Per-atom divisibilities and the closure lemma, exactly:
    X | P^e Y  (Y the only non-coprime atom besides the prime, exponent 1),
    Y | X  (X the only atom on the other side not coprime to Y),
    P^e | X  (X the only atom not coprime to P),  gcd(P, Y) = 1
        ==>  X = +-P^e Y.   Without a prime:  X | Y and Y | X  ==>  X = +-Y."""
    divs = {}
    for side, other in ((Lat, Rat), (Rat, Lat)):
        for A, e in side.items():
            if A == "const":
                continue
            divs[A] = ({B: f for B, f in other.items()
                        if B != "const" and not _coprime(A, B, facts)}, e)
    eqs = []
    for X, (tgt, e) in divs.items():
        if e != 1 or X in (_P, _Q):
            continue
        Ps = {B: f for B, f in tgt.items() if B in (_P, _Q)}
        Ys = {B: f for B, f in tgt.items() if B not in (_P, _Q)}
        if len(Ys) != 1 or len(Ps) > 1:
            continue
        (Y, fy), = Ys.items()
        if fy != 1:
            continue
        backY, eY = divs.get(Y, ({}, 0))
        if eY != 1 or set(backY) != {X}:
            continue
        if Ps:
            (P_, pe), = Ps.items()
            backP, _ = divs.get(P_, ({}, 0))
            if set(backP) != {X} or not _coprime(P_, Y, facts):
                continue
            eqs.append((X, P_**pe * Y))
        else:
            eqs.append((X, Y))
    return divs, eqs


def _pyth_subs(expr):
    """The Pythagorean rewrites available for the symbols in expr:
    U_y^2 -> q^{2y} - V_y^2 etc.  Yields (label, rewritten expr)."""
    yield "id", expr
    for sy in sorted(expr.free_symbols, key=str):
        nm = str(sy)
        if nm[0] not in "UVCS":
            continue
        n = int(nm[1:])
        if nm[0] == "U":
            other, norm = _sp.Symbol(f"V{n}"), _Q**(2 * n)
        elif nm[0] == "V":
            other, norm = _sp.Symbol(f"U{n}"), _Q**(2 * n)
        elif nm[0] == "C":
            other, norm = _sp.Symbol(f"S{n}"), _P**(2 * n)
        else:
            other, norm = _sp.Symbol(f"C{n}"), _P**(2 * n)
        if _sp.degree(expr, sy) >= 2:
            yield f"{nm}^2->", _sp.expand(expr.subs(sy**2, norm - other**2))


def chase(expr, max_terms=6):
    """The divisibility chase on a Lucas equation with up to max_terms
    terms.  Every split of the terms into two sides is tried (after each
    available Pythagorean rewrite); each side is factored into atoms
    (symbols, p, q, polynomial factors), kept only if each side carries at
    most one polynomial atom; divisibilities follow from the coprimality
    oracle and close into equalities X = +-P^e Y (the coincidences);
    each equality is substituted back to give the residual equation.
    Returns the list of (product form, equalities, residuals)."""
    from itertools import combinations
    expr = _sp.expand(expr)
    base_terms = list(_sp.Add.make_args(expr))
    if len(base_terms) > max_terms:
        return {"status": f"{len(base_terms)}-terms", "results": []}
    results = []
    seen = set()
    for label, e2 in _pyth_subs(expr):
        terms = list(_sp.Add.make_args(_sp.expand(e2)))
        n = len(terms)
        if n < 2 or n > max_terms:
            continue
        idx = list(range(n))
        for k in range(1, n // 2 + 1):
            for GL in combinations(idx, k):
                if k * 2 == n and 0 not in GL:
                    continue                      # complementary duplicate
                GR = [j for j in idx if j not in GL]
                left = sum(terms[i] for i in GL)
                right = -sum(terms[j] for j in GR)
                FL, FR = _sp.factor(left), _sp.factor(right)
                Lat, Rat = _atoms(_sp.Mul.make_args(FL)), _atoms(_sp.Mul.make_args(FR))
                polys = [A for A in list(Lat) + list(Rat) if A != "const" and not A.is_Symbol]
                if len(polys) > 2 or any(len(_sp.Add.make_args(A)) > 3 for A in polys):
                    continue
                key = (label, tuple(sorted(str(a) for a in Lat)), tuple(sorted(str(a) for a in Rat)))
                if key in seen:
                    continue
                seen.add(key)
                facts = set()
                for A in list(Lat) + list(Rat):
                    if A != "const" and not A.is_Symbol:
                        _binomial_facts(A, facts)
                divs, eqs = _closure(Lat, Rat, facts)
                if not eqs:
                    continue
                residuals = []
                for X, val in eqs:
                    for sgn in (1, -1):
                        res = _sp.factor(_sp.expand(e2.subs(X, sgn * val)))
                        residuals.append((X, sgn, val, res))
                results.append({"rewrite": label, "L": Lat, "R": Rat, "facts": facts,
                                "divs": divs, "equalities": eqs, "residuals": residuals})
    return {"status": "product-form" if results else "no-equality", "results": results}


def all_collapses(pattern):
    """The collapse identity for EVERY pair of terms (all three hold),
    with the lever bookkeeping relative to that pair.  Returns a list of
    detail dicts in the format of extract()['detail'][0]."""
    terms = cleared_terms(pattern)
    if len(terms) != 3:
        return []
    out = []
    for a, b in ((0, 1), (0, 2), (1, 2)):
        c = ({0, 1, 2} - {a, b}).pop()
        col = find_collapse(terms[a], terms[b])
        if col is None:
            continue
        s, ap, bq, k1, D, k2, M = col
        cc, wpc, wqc, ec, Pc = terms[c]
        ep, eq = wpc - ap, wqc - bq
        absorb = {}
        dead = False
        for P, e, pure in (("p", ep, is_pure_w), ("q", eq, is_pure_l)):
            if e > 0:
                fac = [f for f in (("D", D, k1) if pure(D) else None,
                                   ("M", M, k2) if pure(M) else None) if f]
                if not fac:
                    dead = True
                absorb[P] = ("product", 2 * e, fac)
            elif e < 0:
                if not pure(ec):
                    dead = True
                absorb[P] = ("third", -2 * e, ("C", ec, "Im"))
        out.append({"pair": (a, b), "third": c, "sign": s, "kinds": (k1, k2),
                    "D": D, "M": M, "C": ec, "coeff_c": cc, "absorb": absorb,
                    "dead": dead})
    return out


def classify_equality(X, val):
    """'parity-dead' (odd = even), 'unit-collapse' (X = +-P^e),
    'coincidence-weighted' (X = +-P^e Y), 'coincidence' (X = +-Y),
    or 'rearrangement' (polynomial right-hand side)."""
    def parity(sym):
        n = str(sym)
        return "odd" if n[0] in "UC" else ("even" if n[0] in "VS" else None)
    if not X.is_Symbol:
        return "rearrangement"
    if _sp.expand(val - X) == 0 or _sp.expand(val + X) == 0:
        return "trivial"
    f = _sp.factor(val)
    at = _atoms(_sp.Mul.make_args(f))
    syms = [A for A in at if A != "const" and A not in (_P, _Q)]
    if any(not A.is_Symbol for A in syms):
        return "rearrangement"
    pw = [A for A in at if A in (_P, _Q)]
    if not syms:
        return "unit-collapse"
    if len(syms) == 1:
        Y = syms[0]
        px, py = parity(X), parity(Y)
        if px and py and px != py:
            return "parity-dead"
        return "coincidence-weighted" if pw else "coincidence"
    return "rearrangement"


def _parity_poly(expr):
    """Parity of a polynomial in Lucas symbols and p, q: 'odd' (hence
    nonzero), 'even', or None (undetermined).  U, C, p, q are odd; V, S
    are even; a monomial is odd iff its coefficient is odd and it has no
    V/S factor."""
    expr = _sp.expand(expr)
    odd_count = 0
    for term in _sp.Add.make_args(expr):
        coeff, rest = term.as_coeff_Mul()
        if not coeff.is_integer:
            return None
        if int(coeff) % 2 == 0:
            continue
        has_even = any(str(s)[0] in "VS" for s in rest.free_symbols)
        if not has_even:
            odd_count += 1
    return "odd" if odd_count % 2 == 1 else "even"


def factor_nonzero(f):
    """True if the factor f is provably nonzero: a Lucas symbol (values of
    primitive Gaussian powers never vanish), p, q, a nonzero constant,
    or a polynomial that is odd (hence not 0)."""
    if f.is_number:
        return f != 0
    if f.is_Symbol:
        return True
    return _parity_poly(f) == "odd"


def residual_branches(pattern, coincidences, equations, max_terms=6):
    """For each coincidence X = +-val and each sign, substitute into every
    collapse equation and factor: the branch is DEAD if some equation's
    residual has all factors provably nonzero.  Returns
    {(X, val): {+1: 'dead'|'open', -1: ...}} and the open residuals."""
    out, open_res = {}, {}
    for (X, val) in coincidences:
        if not X.is_Symbol:
            continue
        out[(X, val)] = {}
        for sgn in (1, -1):
            dead = False
            res_list = []
            for e in equations:
                if X not in e.free_symbols:
                    continue
                r = _sp.expand(e.subs(X, sgn * val))
                if r == 0:
                    continue
                fac = _sp.factor(r)
                factors = [f for f in _sp.Mul.make_args(fac)]
                bases = [(f.base if f.is_Pow else f) for f in factors]
                if all(factor_nonzero(b) for b in bases):
                    dead = True
                    break
                res_list.append(fac)
            out[(X, val)][sgn] = "dead" if dead else "open"
            if not dead:
                open_res[(X, val, sgn)] = res_list
    return out, open_res


def run_chase(pattern, max_terms=6):
    """Extract every collapse of the pattern, build each Lucas equation
    (verified against the cleared relation), chase each, and union the
    equalities.  Returns dict: verified count, equalities by class."""
    from collections import Counter
    eqs = {}
    nver = 0
    equations = []
    for d in all_collapses(pattern):
        if d["dead"]:
            return {"status": "DEAD-no-pure-factor", "equalities": {}, "classes": Counter()}
        red, y0, x0, ep, eq, ok = endpoint_identity(pattern, d)
        if not ok:
            continue
        nver += 1
        equations.append(red)
        r = chase(red, max_terms=max_terms)
        for res in r["results"]:
            for X, val in res["equalities"]:
                eqs[(X, val)] = classify_equality(X, val)
    # depth-1 substitution: each derived equality (both signs) into the
    # OTHER collapse equations, then chase again (the hand-proofs'
    # "substitute and re-derive")
    for (X, val), cls in list(eqs.items()):
        if not X.is_Symbol:
            continue
        for sgn in (1, -1):
            for e2 in equations:
                if X not in e2.free_symbols:
                    continue
                e3 = _sp.expand(e2.subs(X, sgn * val))
                if e3 == 0:
                    continue
                r = chase(e3, max_terms=max_terms)
                for res in r["results"]:
                    for X2, val2 in res["equalities"]:
                        if (X2, val2) not in eqs:
                            eqs[(X2, val2)] = classify_equality(X2, val2)
    eqs = {k: v for k, v in eqs.items() if v != "trivial"}
    classes = Counter(eqs.values())
    coincidences = [k for k, v in eqs.items() if v.startswith("coincidence")]
    branches, open_res = residual_branches(pattern, coincidences, equations, max_terms) if coincidences else ({}, {})
    residual_dead = any(all(b[s] == "dead" for s in (1, -1)) for b in branches.values())
    if "parity-dead" in classes:
        status = "DEAD-parity"
    elif residual_dead:
        status = "DEAD-residual"
    elif "unit-collapse" in classes:
        status = "UNIT-COLLAPSE"
    elif coincidences:
        status = "COINCIDENCE"
    elif eqs:
        status = "REARRANGEMENT-ONLY"
    else:
        status = "NO-EQUALITY"
    return {"status": status, "verified": nver, "equalities": eqs, "classes": classes,
            "branches": branches, "open_residuals": open_res}


# ------------------------------------------------- the valuation layer
#
# Every collapse identity is an equality of PRODUCTS,
#     2 p^{2ap} q^{2bq} Trig1(D) Trig2(M) = -c p^{2wpc} q^{2wqc} Im(C),
# so the p-adic and q-adic valuations balance term by term.  Mixed
# monomials are units at both primes; a pure-l monomial is a p-unit and
# a pure-w one a q-unit; and the q-adic valuations of ALL the l-side
# Lucas values are governed by one unknown, the rank of apparition
# r = ord(l/lbar mod rho) (a divisor of q-1), through the lifting-the-
# exponent lemma:
#     v_q(S_n) = v0 + v_q(n/r)      if r | n,  else 0,
#     v_q(C_n) = v0 + v_q(2n/r)     if r | 2n and r !| n,  else 0,
# with v0 = v_q(S_r) >= 1 (S_n = Im l^n, C_n = Re l^n); likewise the
# w-side at p with (r', v0').  The finitely many (r, r') cases give
# linear systems in (v0, v0'); no solution = DEAD by valuation.

def _vsmall(k, P):
    """v_P(k) for a small positive integer k and a specific prime P, or 0
    for a 'generic' prime (P larger than every exponent in play)."""
    if P is None or k <= 0:
        return 0
    v = 0
    while k % P == 0:
        k //= P
        v += 1
    return v


def _lucas_val(kind, n, r, v0, P):
    """Valuation at the OTHER prime of Trig(l^n) with rank of apparition
    r (None = no divisibility at all), base valuation v0 (a symbol or
    int), and specific prime P (None = generic)."""
    if r is None:
        return 0
    n = abs(n)
    if kind == "Im":
        return v0 + _vsmall(n // r, P) if n % r == 0 else 0
    # Re: divisible iff r | 2n and r !| n
    if (2 * n) % r == 0 and n % r != 0:
        return v0 + _vsmall(2 * n // r, P)
    return 0


def collapse_products(pattern):
    """For each pair: (D, k1, M, k2, C, ap, bq, wpc, wqc) -- the product
    identity  +-2 p^{2ap} q^{2bq} T1(D) T2(M) = -c p^{2wpc} q^{2wqc} Im(C)."""
    terms = cleared_terms(pattern)
    out = []
    if len(terms) == 2:
        # doubled pattern: c_a p^.. q^.. Im(A) + c_b p^.. q^.. Im(B) = 0 is a
        # product equality already
        (ca, wpa, wqa, ea, _), (cb, wpb, wqb, eb, _) = terms
        out.append(("doubled", ea, "Im", None, None, eb, wpa, wqa, wpb, wqb))
        return out
    for a, b in ((0, 1), (0, 2), (1, 2)):
        c = ({0, 1, 2} - {a, b}).pop()
        col = find_collapse(terms[a], terms[b])
        if col is None:
            continue
        s, ap, bq, k1, D, k2, M = col
        cc, wpc, wqc, ec, _ = terms[c]
        out.append(("triple", D, k1, M, k2, ec, ap, bq, wpc, wqc))
    return out


def valuation_layer(pattern, max_r=None, specific=(5, 7, 11, 13, 17, 19, 23)):
    """The valuation balance over all (rank, prime-case) configurations.
    Returns {'status': 'DEAD-valuation' | 'SURVIVES', 'survivors': [...]}
    where each survivor is (r_q, q_case, r_p, p_case, v0q, v0p)."""
    prods = collapse_products(pattern)
    if not prods:
        return {"status": "NO-COLLAPSE", "survivors": []}
    exps_l = {abs(m[0]) for pr in prods for m in (pr[1], pr[3], pr[5]) if m is not None and m[0]}
    exps_w = {abs(m[1]) for pr in prods for m in (pr[1], pr[3], pr[5]) if m is not None and m[1]}
    NL = 2 * max(exps_l) if exps_l else 1
    NW = 2 * max(exps_w) if exps_w else 1
    if max_r:
        NL, NW = min(NL, max_r), min(NW, max_r)
    v0q, v0p = _sp.symbols("v0q v0p")

    def val(m, kind, side, r, v0, P):
        """valuation of Trig(monomial m) at prime 'side' ('p' or 'q')."""
        x, y = m
        if side == "p":
            if x != 0:
                return 0                       # involves l: p-unit
            return _lucas_val(kind, y, r, v0, P)
        if y != 0:
            return 0                           # involves w: q-unit
        return _lucas_val(kind, x, r, v0, P)

    survivors = []
    r_cases_l = [None] + list(range(1, NL + 1))
    r_cases_w = [None] + list(range(1, NW + 1))
    q_cases = [None] + [P for P in specific if P <= NL]
    p_cases = [None] + [P for P in specific if P <= NW]
    for rq in r_cases_l:
        for qc in q_cases:
            if rq is not None and qc is not None and (qc - 1) % rq:
                continue                       # r | q - 1
            for rp in r_cases_w:
                for pc in p_cases:
                    if rp is not None and pc is not None and (pc - 1) % rp:
                        continue
                    if qc is not None and pc is not None and qc == pc:
                        continue
                    eqs = []
                    for pr in prods:
                        kind_, D, k1, M, k2, C, ap, bq, wpc, wqc = pr
                        for side, r, v0, P, wl, wr in (("p", rp, v0p, pc, ap, wpc),
                                                       ("q", rq, v0q, qc, bq, wqc)):
                            if kind_ == "doubled":
                                lhs = 2 * wl + val(D, "Im", side, r, v0, P)
                                rhs = 2 * wr + val(C, "Im", side, r, v0, P)
                            else:
                                lhs = 2 * wl + val(D, k1, side, r, v0, P) + val(M, k2, side, r, v0, P)
                                rhs = 2 * wr + val(C, "Im", side, r, v0, P)
                            eqs.append(_sp.expand(lhs - rhs))
                    unknowns = [u for u, r in ((v0q, rq), (v0p, rp)) if r is not None]
                    consts = [e for e in eqs if not e.free_symbols]
                    if any(c != 0 for c in consts):
                        continue
                    lin = [e for e in eqs if e.free_symbols]
                    if not lin:
                        survivors.append((rq, qc, rp, pc, None, None))
                        continue
                    sol = _sp.linsolve(lin, unknowns) if unknowns else None
                    if sol is None or sol == _sp.S.EmptySet:
                        continue
                    ok_sol = None
                    for s in sol:
                        vals = dict(zip(unknowns, s))
                        good = True
                        for u in unknowns:
                            v = vals[u]
                            if v.free_symbols:
                                continue               # free: unconstrained (>= 1 possible)
                            if not (v.is_integer and v >= 1):
                                good = False
                        if good:
                            ok_sol = vals
                    if ok_sol is None:
                        continue
                    survivors.append((rq, qc, rp, pc,
                                      ok_sol.get(v0q) if rq is not None else None,
                                      ok_sol.get(v0p) if rp is not None else None))
    return {"status": "SURVIVES" if survivors else "DEAD-valuation", "survivors": survivors}


# ------------------------------------------- the concentration kill
#
# A pinned system  w^k = P(l, lbar)  (P a Z[i]-polynomial in l = pi^2 and
# its conjugate, e.g. Z+ = l^4 + l^3 lbar - lbar^4) dies by CONCENTRATION
# whenever P - T = cof * lambda^{2a} for a target T = +-lbar^{2j} (then
# lambda = pi) or T = +-l^{2j} (lambda = pibar), a >= 2, with cof small:
#   rho^{2k} - T = (rho^k - tau)(rho^k + tau),  tau^2 = T,  tau a power of
#   the OTHER conjugate;  gcd(A, B) | 2 tau and | 2 rho^k, so gcd | 2;
#   lambda^{2a} lies wholly in one factor, the other divides cof, so its
#   modulus is at most |cof|_max;  A = B +- 2 tau is 0 mod lambda^{2a}, so
#   either B = -+ 2 tau (impossible if 2|tau| > |cof|_max) or
#   |B +- 2 tau| >= p^a, impossible if |cof|_max + 2 p^j < p^a.
# Both size conditions are polynomial inequalities in p = |l| checked for
# all p >= 5 (leading terms) -- so the kill is uniform in k, p, q.

_L, _LB = _sp.symbols("L LB")            # l and lbar as independent variables


def to_l_lbar(expr_c1_s1):
    """Rewrite a polynomial in c1, s1 (and p^2) as a polynomial in L = l,
    LB = lbar via c1 = (L+LB)/2, s1 = (L-LB)/(2i), p^2 = L LB."""
    c1, s1 = _c1, _s1
    e = expr_c1_s1.subs({_P**2: _L * _LB}).subs({c1: (_L + _LB) / 2, s1: (_L - _LB) / (2 * _sp.I)})
    return _sp.expand(e)


def _abs_coeff_bound(poly_in_L_LB):
    """|poly| <= sum |coeff| p^{deg} termwise (|L| = |LB| = p): returns the
    sympy expression in p bounding |poly|."""
    P = _sp.Poly(poly_in_L_LB, _L, _LB)
    tot = 0
    for (dL, dLB), coeff in P.terms():
        tot += _sp.Abs(coeff) * _P**(dL + dLB)
    return _sp.expand(tot)


def concentration_kill(P_l_lbar, jmax=4, amax=6, p_min=5):
    """Search targets T = +-L^{2j}, +-LB^{2j}; if P - T = cof * L^{a} (then
    lambda = pi, needs T a LB-power) or cof * LB^{a} (lambda = pibar, needs
    T an L-power) with a >= 2 and the two size conditions holding for all
    p >= p_min, return the certificate dict; else None."""
    P_ = _sp.expand(P_l_lbar)
    if not P_.is_polynomial(_L, _LB):
        return None
    for j in range(1, jmax + 1):
        for sgn in (1, -1):
            for which, base, other in (("LB", _LB, _L), ("L", _L, _LB)):
                T = sgn * base**(2 * j)
                R = _sp.expand(P_ - T)
                if R == 0:
                    continue
                # divisibility by other^a: the polynomial must have min degree a in `other`
                Rp = _sp.Poly(R, other)
                a = min(m[0] for m in Rp.monoms())
                if a < 2 or a > amax:
                    continue
                cof = _sp.expand(R / other**a)
                bound = _abs_coeff_bound(cof)
                # (i) 2 p^j > |cof|_max   and   (ii) |cof|_max + 2 p^j < p^a, for all p >= p_min
                cond1 = _sp.expand(2 * _P**j - bound)
                cond2 = _sp.expand(_P**a - bound - 2 * _P**j)
                ok = True
                for cnd in (cond1, cond2):
                    poly = _sp.Poly(cnd, _P)
                    # positive for all p >= p_min: positive leading coefficient,
                    # positive at p_min, and NO real root in [p_min, oo)
                    # (exact Sturm count -- no numerics)
                    if poly.LC() <= 0 or cnd.subs(_P, p_min) <= 0:
                        ok = False
                        break
                    if poly.count_roots(inf=p_min) != 0:
                        ok = False
                        break
                if ok:
                    return {"target": f"{'+' if sgn > 0 else '-'}{which}^{2*j}", "lambda": "pi" if other == _L else "pibar",
                            "a": a, "cof": cof, "cof_bound": bound, "tau_abs": f"p^{j}"}
    return None


# ------------------------------------------- the content lemma (tree layer)
#
# A prime r dividing S_x = Im(l^x) satisfies (l/lbar)^x = 1 mod r: the
# "angle" u = l/lbar is a root of unity of order d | x modulo r.  A
# binomial G in the Lucas symbols, written as lbar^m B(u), is then
# divisible by r only if r | B(zeta_d), so gcd(S_x, G) divides
# prod_{d | x} |Res_u(B, Phi_d)|.  For C_x = Re(l^x): u^x = -1, so u has
# order 2d with d | x and x/d odd.  The w-side is the same with w/wbar.

_U = _sp.Symbol("u")


def _angle_poly(G_expr_lucas, side):
    """G (Lucas symbols of one side, p^2 or q^2) -> (m, B(u)) with
    G = LB^m B(u), u = L/LB, B integral (denominators 2^k cleared)."""
    g = lucas_to_L(G_expr_lucas, side)
    g = _sp.expand(g.subs(_L, _U * _LB))
    P = _sp.Poly(g, _LB)
    if P.is_zero:
        return 0, _sp.Integer(0)
    m = min(mon[0] for mon in P.monoms())
    B = _sp.expand(g / _LB**m)
    B = _sp.Poly(B, _U)
    den = 1
    for c in B.all_coeffs():
        c = _sp.nsimplify(c)
        for part in (_sp.re(c), _sp.im(c)):
            part = _sp.Rational(part)
            den = _sp.ilcm(den, part.q)
    return m, _sp.Poly(_sp.expand(B.as_expr() * den), _U)


def content_bound(G_expr_lucas, sym):
    """Bound N on gcd(G, sym) over odd primes r != p, q, from the
    cyclotomic resultants; None if some resultant vanishes (G shares a
    cyclotomic factor with sym: content unbounded)."""
    nm = str(sym)
    x = int(nm[1:])
    side = "l" if nm[0] in "CS" else "w"
    m, B = _angle_poly(G_expr_lucas, side)
    if B.is_zero:
        return None
    N = 1
    if nm[0] in "SV":
        orders = [d for d in range(1, x + 1) if x % d == 0]
    else:
        orders = [2 * d for d in range(1, x + 1) if x % d == 0 and (x // d) % 2 == 1]
    for o in orders:
        phi = _sp.cyclotomic_poly(o, _U)
        res = _sp.expand(_sp.resultant(B.as_expr(), phi, _U))
        # Gaussian-integer resultant: r | B(zeta) in Z[i][zeta] forces
        # r | N(res); use the Gaussian norm as the integer bound
        if res == 0:
            return None
        if res.is_integer:
            N *= int(abs(res))
        else:
            nres = _sp.expand(res * _sp.conjugate(res))
            if not nres.is_integer or nres == 0:
                return None
            N *= int(abs(nres))
    # strip the primes we never need to worry about: 2 (parities), and the
    # frame primes cannot divide S_x/C_x-values of the same side
    while N % 2 == 0:
        N //= 2
    return N


def _closure_content(Lat, Rat, facts):
    """The closure with BOUNDED CONTENT: X | P^e Y, and Y | X * (product
    of polynomial atoms G_i with gcd(Y, G_i) | N_i)  ==>  X = +-P^e Y / d
    for some d | prod N_i (d | Y).  Returns list of (X, P^e Y, N)."""
    divs, _ = _closure(Lat, Rat, facts)
    eqs = []
    for X, (tgt, e) in divs.items():
        if e != 1 or X in (_P, _Q) or not X.is_Symbol:
            continue
        Ps = {B: f for B, f in tgt.items() if B in (_P, _Q)}
        Ys = {B: f for B, f in tgt.items() if B not in (_P, _Q)}
        if len(Ys) != 1 or len(Ps) > 1:
            continue
        (Y, fy), = Ys.items()
        if fy != 1 or not Y.is_Symbol:
            continue
        backY, eY = divs.get(Y, ({}, 0))
        if eY != 1 or X not in backY:
            continue
        others = [B for B in backY if B != X]
        N = 1
        ok = True
        for G in others:
            if G.is_Symbol:
                ok = False
                break
            cb = content_bound(G, Y)
            if cb is None:
                ok = False
                break
            N *= cb
        if not ok:
            continue
        if Ps:
            (P_, pe), = Ps.items()
            backP, _ = divs.get(P_, ({}, 0))
            if set(backP) != {X} or not _coprime(P_, Y, facts):
                continue
            eqs.append((X, P_**pe * Y, N))
        else:
            eqs.append((X, Y, N))
    return eqs


def sliver_kill(P_l_lbar, d, p_min=5):
    """The d > 1 content case: w^k = P/d with P = U + iV, U odd, V even
    and V divisible by p^{2e} (e >= 1, as a polynomial), gcd(U, V) = 1.
    Then (q^k - U)(q^k + U) = V^2 with coprime even factors, the halves
    are {a^2, p^{4e} b^2} with ab = V/2 != 0, so q^k >= p^{4e} + 1; while
    d q^k = |P| <= |P|_max.  Kill if d (p^{4e} + 1) > |P|_max for all
    p >= p_min.  Returns e or None."""
    P_ = _sp.expand(P_l_lbar)
    if not P_.is_polynomial(_L, _LB):
        return None
    V = _sp.expand((P_ - P_.subs(_sp.I, -_sp.I)) / (2 * _sp.I))
    # careful: conjugation of the polynomial in L, LB swaps L <-> LB as well
    Pc = _sp.expand(P_.subs({_L: _LB, _LB: _L, _sp.I: -_sp.I}, simultaneous=True))
    V = _sp.expand((P_ - Pc) / (2 * _sp.I))
    Vp = _sp.Poly(V, _L, _LB)
    if Vp.is_zero:
        return None
    e = min(min(mon) for mon in Vp.monoms())        # power of (L LB) = p^2 dividing V
    if e < 1:
        return None
    bound = _abs_coeff_bound(P_)
    cnd = _sp.expand(d * (_P**(4 * e) + 1) - bound)
    poly = _sp.Poly(cnd, _P)
    if poly.LC() <= 0 or cnd.subs(_P, p_min) <= 0 or poly.count_roots(inf=p_min) != 0:
        return None
    return e


def content_equalities(pattern, max_terms=6):
    """Equalities X = +-P^e Y / d (d | N) from the closure WITH bounded
    content, over all collapses, Pythagorean rewrites and splits."""
    from itertools import combinations
    found = {}
    equations = []
    for d in all_collapses(pattern):
        if d["dead"]:
            return None, []
        red, y0, x0, ep, eq, ok = endpoint_identity(pattern, d)
        if ok:
            equations.append(red)
    for expr in equations:
        for label, e2 in _pyth_subs(expr):
            terms = list(_sp.Add.make_args(_sp.expand(e2)))
            n = len(terms)
            if n < 2 or n > max_terms:
                continue
            idx = list(range(n))
            for k in range(1, n // 2 + 1):
                for GL in combinations(idx, k):
                    if k * 2 == n and 0 not in GL:
                        continue
                    GR = [j for j in idx if j not in GL]
                    FL = _sp.factor(sum(terms[i] for i in GL))
                    FR = _sp.factor(-sum(terms[j] for j in GR))
                    Lat, Rat = _atoms(_sp.Mul.make_args(FL)), _atoms(_sp.Mul.make_args(FR))
                    polys = [A for A in list(Lat) + list(Rat) if A != "const" and not A.is_Symbol]
                    if len(polys) > 2 or any(len(_sp.Add.make_args(A)) > 3 for A in polys):
                        continue
                    facts = set()
                    for A in polys:
                        _binomial_facts(A, facts)
                    for X, val, N in _closure_content(Lat, Rat, facts):
                        if _sp.expand(val - X) == 0 or _sp.expand(val + X) == 0:
                            continue
                        key = (X, val)
                        found[key] = min(found.get(key, N), N)
    return equations, [(X, val, N) for (X, val), N in found.items()]


def pinned_systems(pattern, max_terms=6):
    """For each equality X = +-P^e Y / d (content d | N) whose residual
    pins the partner symbol, return (side, k, d, U, V) with U + iV the
    pinned w^k (or l^k for the mirror types) TIMES d, in Lucas symbols."""
    out = []
    equations, eqs = content_equalities(pattern, max_terms=max_terms)
    if equations is None:
        return "DEAD-no-pure-factor", out
    if not eqs:
        return "NO-EQUALITY", out
    partner_of = {"U": "V", "V": "U", "C": "S", "S": "C"}
    for X, val, N in eqs:
        nm = str(X)
        if nm[0] not in "UVCS":
            continue
        partner = _sp.Symbol(partner_of[nm[0]] + nm[1:])
        side, k = ("w" if nm[0] in "UV" else "l"), int(nm[1:])
        is_re = nm[0] in "UC"
        for dd in [d for d in range(1, N + 1) if N % d == 0]:
            for sgn in (1, -1):
                Xval = sgn * val / dd
                for e in equations:
                    if X not in e.free_symbols:
                        continue
                    res = _sp.factor(_sp.expand(e.subs(X, Xval)))
                    if res == 0:
                        continue
                    factors = [(f.base if f.is_Pow else f) for f in _sp.Mul.make_args(res)]
                    # parity-dead residual for this branch?
                    if all(factor_nonzero(f) for f in factors):
                        continue
                    for f in factors:
                        if partner in f.free_symbols and _sp.degree(f, partner) == 1:
                            sol = _sp.solve(f, partner)
                            if sol:
                                Upart, Vpart = (sgn * val, sol[0] * dd) if is_re else (sol[0] * dd, sgn * val)
                                out.append((side, k, dd, Upart, Vpart))
    return ("COINCIDENCE" if out else "COINCIDENCE-unpinned"), out


def lucas_to_L(expr, side):
    """Lucas symbols of one side -> polynomial in L, LB (l, lbar for the
    l-side; for the w-side the same letters stand for w, wbar and the
    prime power symbol q^2 = L LB)."""
    subs = {}
    for s in expr.free_symbols:
        nm = str(s)
        if nm[0] in "UVCS":
            n = int(nm[1:])
            if nm[0] in "UC":
                subs[s] = (_L**n + _LB**n) / 2
            else:
                subs[s] = (_L**n - _LB**n) / (2 * _sp.I)
    e = expr.subs(subs)
    e = e.subs({_P**2: _L * _LB, _Q**2: _L * _LB})
    return _sp.expand(e)


def kill_pattern(pattern, jmax=6, amax=12):
    """End-to-end: valuation layer, chase + residual parity, then the
    concentration kill on every pinned system (all sign/conjugate
    variants).  Returns (verdict, details)."""
    v = valuation_layer(pattern)
    if v["status"] == "DEAD-valuation":
        return "DEAD-valuation", None
    r = run_chase(pattern)
    if r["status"] in ("DEAD-parity", "DEAD-residual"):
        return r["status"], None
    status, systems = pinned_systems(pattern)
    if status != "COINCIDENCE":
        # last resort before giving up: the general unit collapse on a lever
        try:
            uc = unit_collapse_kill(pattern)
        except Exception:
            uc = None
        if uc and "kills" in uc:
            return "DEAD-unit-collapse", uc
        wk = _window_stage(pattern)
        if wk:
            return "DEAD-window", wk
        rv, rc = _residual_stage(pattern)
        if rv:
            return rv, rc
        return status, None
    # group the pinned branches by the equality they come from: a pattern
    # is dead as soon as ONE equality has every (sign, content) branch dead
    groups = {}
    for side, k, dd, U, V in systems:
        groups.setdefault((side, k, str(U).replace("-", "")), []).append((side, k, dd, U, V))
    certs = []
    for key, branches in groups.items():
        all_dead = True
        for side, k, dd, U, V in branches:
            P_ = _sp.cancel(lucas_to_L(U + _sp.I * V, "l" if side == "w" else "w"))
            if not P_.is_polynomial(_L, _LB):
                all_dead = False
                certs.append((side, k, dd, 0, False, None))
                break
            P_ = _sp.expand(P_)
            for sg in (1, -1):
                for cj in (False, True):
                    PP = sg * P_
                    if cj:
                        PP = PP.subs({_L: _LB, _LB: _L}, simultaneous=True)
                    PP = _sp.expand(PP)
                    c = None
                    if dd == 1:
                        c = concentration_kill(PP, jmax=jmax, amax=amax)
                    if c is None:
                        e = sliver_kill(PP, dd)
                        c = {"sliver": e, "d": dd} if e else None
                    certs.append((side, k, dd, sg, cj, c))
                    if c is None:
                        all_dead = False
            if not all_dead:
                break
        if all_dead:
            return "DEAD-concentration", certs
    # a pinned coincidence system is not a kill by itself: the window finisher
    # may still close the pattern (H3's opposite-sign children do die here)
    wk = _window_stage(pattern)
    if wk:
        return "DEAD-window", wk
    rv, rc = _residual_stage(pattern)
    if rv:
        return rv, rc
    return "COINCIDENCE-open", certs


def _residual_stage(pattern):
    """The RESIDUAL finisher (entry 88, build B): a collapse equation linear
    in the legs of one index of one side forces the rigid Gaussian form
    X^k = +-(B - iA)/g, killed by parity or by the concentration/sliver
    certifiers -- compute/residual_kill.py.  Returns (verdict, cert) or
    (None, None)."""
    try:
        from compute.residual_kill import residual_kill
        v, cert = residual_kill(pattern)
    except Exception:
        return None, None
    if v in ("DEAD-residual-parity", "DEAD-residual-concentration"):
        return v, cert
    return None, None


def _window_stage(pattern):
    """The WINDOW finisher (entry 86): levers on any collapse, pincers, size
    windows, Fermat pins, index-3 cofactor pairs -- compute/window_kill.py.
    Returns the certificate when it kills, else None."""
    try:
        from compute.window_kill import window_kill
        wk = window_kill(pattern)
    except Exception:
        return None
    return wk if (wk and wk.get("kills")) else None


# ------------------------------------------- Block B: the unit collapse
#
# The four Block-B children of A3.10 carry a q^4 lever on the l-side:
# after cancelling a common factor the collapse reads  T * M = -+2 Y q^4 C2
# with M = Im(l w^4)-type a q-unit, T in {C1^2 - 3 S1^2, 3 C1^2 - S1^2}
# odd and coprime to Y and C2, so T = +-q^4 (a UNIT COLLAPSE); and
# T = p^2 - 4 s1^2 or 4 c1^2 - p^2 splits into coprime factors
# {p -+ 2 s1} or {2 c1 -+ p} that must be {1, q^4}, leaving
# c1^2 (or s1^2) = (3 q^4 +- 1)(q^4 +- 3)/16 -- dead 2-adically.

def block_b_lemma(pattern):
    """Machine-verified kill of a Block-B child.  Returns the certificate
    dict; raises AssertionError if any step fails."""
    c1, s1 = _sp.symbols("c1 s1", real=True)
    qq = _sp.Symbol("q", positive=True)
    C1, S1, C2 = _sp.Symbol("C1"), _sp.Symbol("S1"), _sp.Symbol("C2")
    cert = {"pattern": pattern}
    # 1. the q-lever collapse equation
    red = None
    for d in all_collapses(pattern):
        e, y0, x0, ep, eq, ok = endpoint_identity(pattern, d)
        if ok and _Q in e.free_symbols:
            red = e
            break
    assert red is not None, "no q-lever collapse"
    expr = _sp.expand(red)
    qpart = sum(t for t in _sp.Add.make_args(expr) if _Q in t.free_symbols)
    rest = _sp.expand(expr - qpart)
    FL, FR = _sp.factor(rest), _sp.factor(-qpart)
    atomsL = _atoms(_sp.Mul.make_args(FL))
    atomsR = _atoms(_sp.Mul.make_args(FR))
    # 2. structure: rest = const * X * T * M ; -qpart = const * C1 * S1 * q^4 * (C1-S1)(C1+S1)
    symsL = [a for a in atomsL if a != "const"]
    X = [a for a in symsL if a in (C1, S1)]
    assert len(X) == 1, atomsL
    X = X[0]
    Y = S1 if X == C1 else C1
    T = [a for a in symsL if not a.is_Symbol and all(str(s)[0] in "CS" for s in a.free_symbols)]
    M = [a for a in symsL if not a.is_Symbol and any(str(s)[0] in "UV" for s in a.free_symbols)]
    assert len(T) == 1 and len(M) == 1, atomsL
    T, M = T[0], M[0]
    assert atomsR.get(_Q, 0) == 4 and atomsR.get(C1, 0) == 1 and atomsR.get(S1, 0) == 1, atomsR
    others = [a for a in atomsR if a not in (_Q, C1, S1, "const")]
    assert set(map(str, others)) == {"C1 - S1", "C1 + S1"}, others
    cert["T"], cert["M"], cert["cancel"] = str(T), str(M), str(X)
    # 3. unit and coprimality facts
    assert is_unit_at(M, _Q), "M not a q-unit"
    assert _parity_poly(T) == "odd", "T not odd"
    assert content_bound(T, Y) == 1, ("gcd(T, Y)", content_bound(T, Y))
    assert content_bound(T, C2) == 1, ("gcd(T, C2)", content_bound(T, C2))
    # hence q^4 | T M with M a q-unit => q^4 | T; and T | 2 Y q^4 C2 with T odd,
    # coprime to Y and C2 => T | q^4  =>  T = +-q^4  (unit collapse)
    # 4. the Z-form of T and the coprime split
    Tcs = _sp.expand(T.subs({C1: c1, S1: s1}))
    p2 = c1**2 + s1**2
    if _sp.expand(Tcs - (p2 - 4 * s1**2)) == 0:
        kind = "p2-4s1^2"
    elif _sp.expand(Tcs - (4 * c1**2 - p2)) == 0:
        kind = "4c1^2-p2"
    else:
        raise AssertionError(("T form", Tcs))
    cert["form"] = kind
    # factors (p - 2 s1)(p + 2 s1) = eps q^4  [or (2 c1 - p)(2 c1 + p)]: odd, coprime
    # (a common divisor divides 2p and q^4), so {|small|, large} = {1, q^4}
    p_, v = _sp.symbols("p v", positive=True)
    for eps in (1, -1):
        if kind == "p2-4s1^2":
            # p - 2 s1 = eps (small factor = eps), p + 2 s1 = q^4
            psol, ssol = (qq**4 + eps) / 2, (qq**4 - eps) / 4
            other_sq = _sp.expand(psol**2 - ssol**2)       # = c1^2
        else:
            # 2 c1 - p = eps, 2 c1 + p = q^4
            csol, psol = (qq**4 + eps) / 4, (qq**4 - eps) / 2
            other_sq = _sp.expand(psol**2 - csol**2)       # = s1^2
        sixteen = _sp.factor(_sp.expand(16 * other_sq))
        # it must be (3 q^4 +- 1)(q^4 +- 3): coprime odd parts, so q^4 +- 3 has square odd part
        cert[f"eps={eps}"] = str(sixteen)
        f1 = _sp.expand(3 * qq**4 + (eps if kind == "p2-4s1^2" else -eps))
        f2 = _sp.expand(qq**4 + (3 * eps if kind == "p2-4s1^2" else -3 * eps))
        assert _sp.expand(f1 * f2 - 16 * other_sq) == 0, (sixteen, f1, f2)
        # 2-adic kill of q^4 + 3 eps' = 2^b v^2 (v odd), eps' = sign in f2
        e2 = 3 if _sp.expand(f2 - (qq**4 + 3)) == 0 else -3
        # residues of q^4 + e2 mod 16 over odd q are all equal to 4 (e2 = 3) or 14 (e2 = -3)
        res = {(q0**4 + e2) % 16 for q0 in range(1, 16, 2)}
        assert res == ({4} if e2 == 3 else {14}), res
        if e2 == 3:
            # 4 v^2 = q^4 + 3  =>  (2v - q^2)(2v + q^2) = 3, impossible for q >= 2 (2v + q^2 > 3)
            cert["kill+"] = "q^4+3 = 4v^2 => (2v-q^2)(2v+q^2) = 3 impossible"
        else:
            # 2 v^2 = q^4 - 3 => v^2 = 7 mod 8, impossible
            assert 7 not in {x * x % 8 for x in range(8)}
            cert["kill-"] = "q^4-3 = 2v^2 => v^2 = 7 mod 8 impossible"
    return cert


# ------------------------------------------- the general unit collapse
#
# Generalizes block_b_lemma.  A lever equation with prime P (q for an
# l-side collapse) factors as  const * (one-sided atoms) * T * M
#   = const' * (one-sided atoms) * P^{2e},
# with M a P-unit (mixed) and T the one one-sided polynomial atom that
# is NOT a structural P-unit.  If every other atom is coprime to T (the
# content bounds are 1) and T is odd, then T | c P^{2e} and P^{2e} | T,
# so T = +-c' P^{2e} with c' | c.  Writing T as a quadratic form in
# (C_x, S_x) with p^{2x} = C_x^2 + S_x^2, a difference of squares
# a^2 p^{2x} - b^2 S_x^2 (or with C_x) splits into coprime factors, each
# +- a divisor of c' P^{2e}; the finitely many cases give
# C_x^2 (or S_x^2) = R(P) with R a polynomial in P^{2e}, and R is killed
# by exact modular square tests or by the small-difference size kill.

def _never_square_mod(R, var, moduli=(16, 32, 9, 5, 7, 11, 13, 64, 27, 25)):
    """True if R(var) is never a square modulo some m for var coprime to m
    (var ranges over units mod m, since var is a prime >= 5 here)."""
    from math import gcd
    for m in moduli:
        sq = {(x * x) % m for x in range(m)}
        ok = True
        for t in range(m):
            if gcd(t, m) != 1:
                continue
            val = int(R.subs(var, t)) % m
            if val in sq:
                ok = False
                break
        if ok:
            return m
    return None


def _small_square_difference_kill(Ra, Rb, var):
    """Kill of  A^2 = Ra(var), B^2 = Rb(var)  when Ra - Rb (or a fixed
    linear combination) is a small constant: two squares of moduli
    > sqrt(const) cannot differ by it.  Returns True if certified."""
    diff = _sp.expand(Ra - Rb)
    if diff.is_number and diff != 0:
        # A^2 - B^2 = diff  =>  (A - B)(A + B) = diff, so A + B <= |diff|,
        # impossible once Ra(var) > diff^2 for the smallest admissible var
        c = abs(int(diff))
        for v0 in (5, 7, 11, 13):
            if Ra.subs(var, v0) > c * c:
                return True
    return False


def content_bound_poly(T, G, side="l"):
    """gcd(T, G) bound for two polynomials of the SAME side: a prime r
    dividing both makes u = l/lbar a common root of their angle
    polynomials mod r, so r | Res_u(B_T, B_G); returns the odd part of the
    Gaussian norm of the resultant (None if the resultant vanishes)."""
    mT, BT = _angle_poly(T, side)
    mG, BG = _angle_poly(G, side)
    if BT.is_zero or BG.is_zero:
        return None
    res = _sp.expand(_sp.resultant(BT.as_expr(), BG.as_expr(), _U))
    if res == 0:
        return None
    if res.is_integer:
        N = int(abs(res))
    else:
        n_ = _sp.expand(res * _sp.conjugate(res))
        if not n_.is_integer or n_ == 0:
            return None
        N = int(abs(n_))
    while N % 2 == 0:
        N //= 2
    return N


def _twopow_square_kill(f, var, kmax=8, moduli=(8, 16, 32, 64, 3, 5, 7, 9, 11, 13)):
    """Certify that f(var) = 2^k v^2 is impossible for every k <= kmax
    (var a prime >= 5): for each k, an exact modular test (f(t) is never
    2^k times a square mod m over units t), or the size kill when f is
    X^2 + c with X a monomial in var and c a small constant.  Returns the
    list of per-k certificates, or None if some k survives."""
    from math import gcd
    certs = []
    fp = _sp.Poly(f, var)
    # X^2 + c shape?
    monoms = fp.monoms()
    shape = None
    if len(monoms) == 2 and monoms[-1] == (0,) and monoms[0][0] % 2 == 0 and fp.LC() == 1:
        c0 = int(fp.coeff_monomial(1))
        shape = (monoms[0][0] // 2, c0)
    for k in range(0, kmax + 1):
        done = None
        for m in moduli:
            sq2 = {(2**k * x * x) % m for x in range(m)}
            if all(int(f.subs(var, t)) % m not in sq2 for t in range(m) if gcd(t, m) == 1):
                done = f"mod {m}"
                break
        if done is None and shape is not None and k % 2 == 0:
            # (2^{k/2} v)^2 - X^2 = c: two squares differing by |c| need 2^{k/2} v + X <= |c|,
            # impossible since X = var^{shape} >= 5^{shape} > |c|
            half, c0 = shape
            if 5**half > abs(c0) and c0 != 0:
                done = f"size: (2^{k//2}v - var^{half})(2^{k//2}v + var^{half}) = {c0}"
        if done is None:
            return None
        certs.append((k, done))
    return certs


def _square_residual_kill(R, var):
    """R(var) (rational coefficients) must be a perfect square (times den^{-1}):
    with den * R = Rint, Rint must be den * square.  Factor Rint over Z; if the
    factors are pairwise coprime up to 2-powers (resultants are powers of 2)
    then each odd-multiplicity factor is 2^k * square; kill each such factor
    for every k.  Returns a certificate dict or None."""
    den = 1
    for c in _sp.Poly(R, var).all_coeffs():
        den = _sp.ilcm(den, _sp.Rational(c).q)
    Rint = _sp.expand(R * den)
    fac = _sp.factor_list(Rint)
    factors = [(f, m) for f, m in fac[1] if _sp.Poly(f, var).degree() > 0]
    # pairwise resultants must be powers of 2 (then odd parts are pairwise coprime)
    for i in range(len(factors)):
        for j in range(i + 1, len(factors)):
            r = _sp.resultant(factors[i][0], factors[j][0], var)
            r = abs(int(r))
            while r % 2 == 0 and r:
                r //= 2
            if r != 1:
                return None
    # the constant content's odd part must also be a square times ... (ignore: it only
    # adds a fixed odd square factor requirement; we only need ONE factor to die)
    for f, m in factors:
        if m % 2 == 1:
            certs = _twopow_square_kill(f, var)
            if certs is not None:
                return {"den": int(den), "factor": str(f), "certs": certs}
    return None


def unit_collapse_kill(pattern):
    """General unit collapse + coprime split + finishers.  Returns a
    certificate dict or None (with 'why' when the shape does not fit)."""
    qq = _sp.Symbol("q", positive=True)
    pp = _sp.Symbol("p", positive=True)
    cert = {"pattern": pattern}
    for d in all_collapses(pattern):
        e, y0, x0, ep, eq, ok = endpoint_identity(pattern, d)
        if not ok:
            continue
        for P_ in (_Q, _P):
            if P_ not in e.free_symbols:
                continue
            expr = _sp.expand(e)
            ppart = sum(t for t in _sp.Add.make_args(expr) if P_ in t.free_symbols)
            rest = _sp.expand(expr - ppart)
            if rest == 0:
                continue
            FL, FR = _sp.factor(rest), _sp.factor(-ppart)
            atomsL = {a: m for a, m in _atoms(_sp.Mul.make_args(FL)).items() if a != "const"}
            atomsR = {a: m for a, m in _atoms(_sp.Mul.make_args(FR)).items() if a != "const"}
            cL = _atoms(_sp.Mul.make_args(FL)).get("const", 1)
            cR = _atoms(_sp.Mul.make_args(FR)).get("const", 1)
            side_letters = "CS" if P_ == _Q else "UV"      # the lever prime's OTHER side
            other_letters = "UV" if P_ == _Q else "CS"
            # cancel common atoms
            for a in list(atomsL):
                if a in atomsR:
                    m = min(atomsL[a], atomsR[a])
                    atomsL[a] -= m
                    atomsR[a] -= m
            atomsL = {a: m for a, m in atomsL.items() if m}
            atomsR = {a: m for a, m in atomsR.items() if m}
            e2 = atomsR.pop(P_, 0)
            if e2 == 0 or P_ in atomsL:
                continue
            # classify the left atoms
            def side_of(a):
                letters = {str(s)[0] for s in a.free_symbols if s not in (_P, _Q)}
                if letters <= set(side_letters):
                    return "same"
                if letters <= set(other_letters):
                    return "other"
                return "mixed"
            T_cands, units_ok = [], True
            for a, m in atomsL.items():
                if a.is_Symbol:
                    if str(a)[0] in side_letters:
                        T_cands.append((a, m))     # a bare symbol could carry P too
                    continue
                s = side_of(a)
                if s == "same":
                    if is_unit_at(a, P_):
                        continue
                    T_cands.append((a, m))
                elif not is_unit_at(a, P_):
                    units_ok = False
            if not units_ok:
                continue
            # right side atoms must all be P-units or bare same-side symbols coprime to T
            if len(T_cands) != 1 or T_cands[0][1] != 1:
                continue
            T = T_cands[0][0]
            if T.is_Symbol:
                continue
            bad = False
            sidename = "l" if side_letters == "CS" else "w"
            for a in atomsR:
                if a.is_Symbol:
                    if str(a)[0] in side_letters and content_bound(T, a) != 1:
                        bad = True
                    elif str(a)[0] in other_letters:
                        pass                        # other-side symbol: a P-unit structurally
                elif side_of(a) == "same":
                    if content_bound_poly(T, a, sidename) != 1:
                        bad = True
                elif not is_unit_at(a, P_):
                    bad = True
            if bad or _parity_poly(T) != "odd":
                continue
            # hence T | cR * P^{2e} (T coprime to everything else, odd) and P^{2e} | T:
            # T = +-c' P^{2e}, c' | cR (and c' odd)
            cR_odd = abs(int(cR))
            while cR_odd % 2 == 0:
                cR_odd //= 2
            divisors = [c for c in range(1, cR_odd + 1) if cR_odd % c == 0]
            # T as a form in (C_x, S_x): find x
            syms = [s for s in T.free_symbols if s not in (_P, _Q)]
            xs = {int(str(s)[1:]) for s in syms}
            if len(xs) != 1:
                continue
            x = xs.pop()
            Cx, Sx = _sp.Symbol(side_letters[0] + str(x)), _sp.Symbol(side_letters[1] + str(x))
            Pown = pp if P_ == _Q else qq                 # the prime of T's own side
            cert.update({"prime": str(P_), "e": e2, "T": str(T), "x": x, "cR": int(cR)})
            # quadratic form alpha C^2 + beta S^2 (+ gamma p^{2x} allowed via symbols p, q)
            Tp = _sp.Poly(T, Cx, Sx)
            if Tp.total_degree() != 2 or any(sum(mon) not in (0, 2) for mon in Tp.monoms()):
                continue
            alpha = Tp.coeff_monomial(Cx**2)
            beta = Tp.coeff_monomial(Sx**2)
            gamma = _sp.expand(T - alpha * Cx**2 - beta * Sx**2)     # multiple of P_own^{2x}
            # substitute C^2 = P_own^{2x} - S^2:  T = (alpha + gamma/P^{2x}) P^{2x} + (beta - alpha) S^2
            g = _sp.expand(gamma / Pown**(2 * x)) if gamma != 0 else 0
            A = _sp.nsimplify(alpha + g)
            B = _sp.nsimplify(beta - alpha)
            # difference of squares needs A = a^2 > 0 and -B = b^2 > 0  (T = a^2 P^{2x} - b^2 S^2),
            # or the mirror with C: T = (beta + g) P^{2x} + (alpha - beta) C^2
            variants = []
            # T = +-c' P^e, so the overall sign of T is free: try T and -T
            for sT in (1, -1):
                As, Bs = sT * A, sT * B
                if As.is_integer and As > 0 and (-Bs).is_integer and -Bs > 0 and _sp.sqrt(As).is_integer and _sp.sqrt(-Bs).is_integer:
                    variants.append(("S", int(_sp.sqrt(As)), int(_sp.sqrt(-Bs))))
                A2, B2 = sT * _sp.nsimplify(beta + g), sT * _sp.nsimplify(alpha - beta)
                if A2.is_integer and A2 > 0 and (-B2).is_integer and -B2 > 0 and _sp.sqrt(A2).is_integer and _sp.sqrt(-B2).is_integer:
                    variants.append(("C", int(_sp.sqrt(A2)), int(_sp.sqrt(-B2))))
            if not variants:
                cert["why"] = "T not a difference of squares"
                continue
            for which, a, b in variants:
                # (a P^x - b Y)(a P^x + b Y) = +-c' P_^{2e},  Y = S_x or C_x; coprime up to gcd | 2ab
                kills = {}
                for cprime in divisors:
                    for eps in (1, -1):
                        # small factor = +-t1, large = t2 P_^{2e} with t1 t2 = c', or both split
                        # enumerate all factor pairs (u, v) with u v = eps c' P_^{2e}, u = small:
                        for t1 in [t for t in range(1, cprime + 1) if cprime % t == 0]:
                            t2 = cprime // t1
                            for s1 in (1, -1):
                                # a P^x - b Y = s1 t1,  a P^x + b Y = eps s1 t2 P_^{2e}
                                Px = (s1 * t1 + eps * s1 * t2 * P_**e2) / (2 * a)
                                Y = (eps * s1 * t2 * P_**e2 - s1 * t1) / (2 * b)
                                # the other coordinate squared: P^{2x} - Y^2 (as a polynomial in P_)
                                R = _sp.expand(Px**2 - Y**2)
                                key = (which, cprime, eps, t1, s1)
                                if R.is_number:
                                    kills[key] = "constant" if R < 0 or not _sp.sqrt(R).is_integer else None
                                    continue
                                c_ = _square_residual_kill(R, P_)
                                kills[key] = (f"factor {c_['factor']} of {c_['den']}*R is never 2^k*square: "
                                              f"{c_['certs']}") if c_ else None
                if all(v is not None for v in kills.values()) and kills:
                    cert.update({"variant": which, "a": a, "b": b, "kills": kills})
                    return cert
                cert["partial"] = {k: v for k, v in kills.items()}
    cert.setdefault("why", "no unit-collapse lever or unfinished cases")
    return None if "kills" not in cert else cert


def box_classes(a, b):
    return [(j, k) for j in range(0, a + 1) for k in range(-b, b + 1)
            if (j, k) != (0, 0) and (j > 0 or k > 0)]


def survey_box(a, b, mods=(16, 32, 64, 9, 5, 7, 11, 13, 8, 3)):
    """The engine's general layers (valuation -> tan-half factorization ->
    congruence) with the complete enumeration and canon_full dedup.
    Returns (verdict counts, list of OPEN (pattern, kind))."""
    from collections import Counter
    from compute.two_prime_additive import (
        candidates_for_box, enumerate_patterns_complete, canon_full,
        valuation_pruned, relation_poly, peel_general, is_constant,
        residual_cs_form, congruence_kill)
    cls = box_classes(a, b)
    cands = candidates_for_box(a, b)
    seen, verdict, opens = set(), Counter(), []
    for pattern, kind in enumerate_patterns_complete(cls):
        key = canon_full(pattern)
        if key in seen:
            continue
        seen.add(key)
        if valuation_pruned(pattern):
            verdict["VALUATION"] += 1
            continue
        N = relation_poly(pattern)
        if not N:
            verdict["ZERO"] += 1
            continue
        factors, residual = peel_general(N, cands)
        if is_constant(residual):
            verdict["FACTORED"] += 1
            continue
        G = residual_cs_form(residual)
        if any(congruence_kill(G, M) for M in mods):
            verdict["CONGRUENCE"] += 1
            continue
        verdict["OPEN"] += 1
        opens.append((pattern, kind))
    return verdict, opens


def shape(m):
    return "w" if is_pure_w(m) else ("l" if is_pure_l(m) else "mixed")


def type_census(opens):
    """Run the extractor on the distinct OPEN patterns; returns
    (status counts, family signature counts, shape-type counts)."""
    from collections import Counter
    st, fams, types = Counter(), Counter(), Counter()
    for pattern, kind in opens:
        if kind != "distinct":
            continue
        r = extract(tuple(pattern))
        st[r["status"]] += 1
        if r["status"] != "ENDPOINT":
            continue
        d = r["detail"][0]
        fams[endpoint_signature(r)] += 1
        types[(shape(d["D"]), shape(d["M"]), shape(d["C"]),
               tuple(sorted(d["absorb"])))] += 1
    return st, fams, types


def endpoint_signature(r):
    """A hashable family signature for an ENDPOINT record."""
    d = r["detail"][0]
    ab = tuple(sorted((P, v[0], v[1], tuple(f[0] for f in v[2]) if v[0] == "product" else v[2][0])
                      for P, v in d["absorb"].items()))
    return (d["kinds"], d["D"], d["M"], d["C"], ab)
