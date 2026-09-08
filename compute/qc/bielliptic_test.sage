r"""THE GENERAL BIELLIPTIC TEST for a genus-2 curve y^2 = f(x), f of degree 5 or 6 over Q (entry 131).
A non-hyperelliptic involution of the curve is a Moebius involution sigma of P^1 permuting the six
branch points (the roots of f, with infinity when deg f = 5).  A Moebius map interchanging two points
is an involution, and is determined by two interchanged pairs; so every candidate comes from one of the
15 perfect matchings of the six points into three pairs: build sigma from the first two pairs (exactly,
over QQbar), keep it if it also interchanges the third.  sigma is defined over Q iff its matrix is
proportional to a rational one; its fixed points are rational iff a^2 + bc is a rational square
(sigma = (ax + b)/(cx - a)); then the coordinate change x' = (x - p)/(x - q) sending the fixed points to
0 and infinity makes sigma into x' -> -x' and the model even, y^2 = g(x'^2), as the QC pipeline needs.
Usage: sage bielliptic_test.sage <json list of coefficient lists, highest degree first> <out json>"""
import sys, json
from itertools import combinations

def matchings(items):
    if not items:
        yield []
        return
    a = items[0]
    for i in range(1, len(items)):
        b = items[i]
        rest = items[1:i] + items[i+1:]
        for m in matchings(rest):
            yield [(a, b)] + m

def proportional(v, w):
    return v[0]*w[1] - v[1]*w[0] == 0

def involution_from(P1, Q1, P2, Q2):
    rows = []
    for v, w in ((P1, Q1), (Q1, P1), (P2, Q2)):
        rows.append([v[0]*w[1], v[1]*w[1], -v[0]*w[0], -v[1]*w[0]])
    A = matrix(QQbar, rows)
    K = A.right_kernel()
    if K.dimension() != 1:
        return None
    a, b, c, d = K.basis()[0]
    M = matrix(QQbar, [[a, b], [c, d]])
    if M.determinant() == 0:
        return None
    return M

def apply(M, v):
    w = M * vector(QQbar, v)
    return (w[0], w[1])

def normalize(M):
    for i in range(2):
        for j in range(2):
            if M[i, j] != 0:
                return M / M[i, j]
    return M

def rational_matrix(M):
    Mn = normalize(M)
    try:
        return matrix(QQ, [[QQ(Mn[0, 0]), QQ(Mn[0, 1])], [QQ(Mn[1, 0]), QQ(Mn[1, 1])]])
    except (TypeError, ValueError):
        return None

def analyse(coeffs):
    R.<x> = QQ[]
    f = R(list(reversed(coeffs)))
    deg = f.degree()
    assert deg in (5, 6) and f.is_squarefree()
    pts = [(r, QQbar(1)) for r in f.roots(QQbar, multiplicities=False)]
    if deg == 5:
        pts.append((QQbar(1), QQbar(0)))
    assert len(pts) == 6
    invols = []
    for m in matchings(list(range(6))):
        (i1, j1), (i2, j2), (i3, j3) = m
        M = involution_from(pts[i1], pts[j1], pts[i2], pts[j2])
        if M is None:
            continue
        if not (proportional(apply(M, pts[i3]), pts[j3]) and proportional(apply(M, pts[j3]), pts[i3])):
            continue
        if M.trace() != 0:
            continue
        Mn = normalize(M)
        if not any((Mn - N).is_zero() for N in invols):
            invols.append(Mn)
    out = {"f": coeffs, "degree": int(deg), "n_involutions": len(invols), "involutions": []}
    S.<X, Z> = QQ[]
    F = sum(QQ(c) * X^k * Z^(6 - k) for k, c in enumerate(reversed(coeffs)))
    for M in invols:
        Mq = rational_matrix(M)
        rec = {"rational": Mq is not None}
        if Mq is None:
            rec["matrix"] = [str(M[0, 0]), str(M[0, 1]), str(M[1, 0]), str(M[1, 1])]
            out["involutions"].append(rec)
            continue
        a, b, c = Mq[0, 0], Mq[0, 1], Mq[1, 0]
        rec["matrix"] = [str(a), str(b), str(c), str(Mq[1, 1])]
        disc = a^2 + b*c
        rec["fixed_points_rational"] = disc.is_square()
        if disc.is_square():
            s = disc.sqrt()
            if c != 0:
                p, q = (a + s) / c, (a - s) / c          # fixed points of (ax+b)/(cx-a): c x^2 - 2a x - b = 0
                Fp = F(q*X - p*Z, X - Z)
            else:
                p = -b / (2*a)                            # sigma(x) = -x - b/a: fixed points p and infinity
                Fp = F(X + p*Z, Z)
            g = S(Fp(X, 1))
            gx = R([g.monomial_coefficient(X^k) for k in range(7)])
            rec["fixed_points"] = [str(p), str(q) if c != 0 else "inf"]
            rec["even_model"] = [str(gx[k]) for k in (6, 4, 2, 0)]
            rec["even"] = all(gx[k] == 0 for k in (1, 3, 5))
            if rec["even"] and gx.degree() == 6:
                # scale to integers: x = X/l, y -> l^3 y
                cs = [gx[6], gx[4], gx[2], gx[0]]
                den = lcm([QQ(v).denominator() for v in cs])
                l = 1
                while any((QQ(v) * l^(6 - k)).denominator() != 1 for v, k in zip(cs, (6, 4, 2, 0))):
                    l += 1
                a6, a4, a2, a0 = [ZZ(QQ(v) * l^(6 - k)) for v, k in zip(cs, (6, 4, 2, 0))]
                gg = gcd([a6, a4, a2, a0])
                sq = 1
                for pp, e in factor(gg):
                    sq *= pp^(2 * (e // 2))
                a6, a4, a2, a0 = [ZZ(v / sq) for v in (a6, a4, a2, a0)]
                rec["even_integral"] = [int(a6), int(a4), int(a2), int(a0)]
                E1 = EllipticCurve([0, a4, 0, a2*a6, a0*a6^2]); E2 = EllipticCurve([0, a2, 0, a0*a4, a0^2*a6])
                rec["E1"] = {"label": E1.cremona_label() if E1.conductor() < 500000 else None, "conductor": int(E1.conductor()), "rank": int(E1.rank()), "torsion": int(E1.torsion_order())}
                rec["E2"] = {"label": E2.cremona_label() if E2.conductor() < 500000 else None, "conductor": int(E2.conductor()), "rank": int(E2.rank()), "torsion": int(E2.torsion_order())}
                Rx.<xx> = QQ[]
                fe = a6*xx^6 + a4*xx^4 + a2*xx^2 + a0
                Hc = HyperellipticCurve(fe)
                rec["small_points"] = [str(P) for P in Hc.rational_points(bound=200)]
        out["involutions"].append(rec)
    return out

curves = json.loads(sys.argv[1]) if len(sys.argv) > 1 else json.load(open("/home/will/qc_runs/odd_quintics_in.json"))
results = []
for coeffs in curves:
    r = analyse(coeffs)
    results.append(r)
    print(r["f"], "-> involutions:", r["n_involutions"], [(i.get("rational"), i.get("fixed_points_rational"), i.get("even_integral"), i.get("E1", {}).get("label"), i.get("E1", {}).get("rank"), i.get("E2", {}).get("label"), i.get("E2", {}).get("rank")) for i in r["involutions"]], flush=True)
json.dump(results, open(sys.argv[2] if len(sys.argv) > 2 else "/home/will/qc_runs/bielliptic_test_out.json", "w"), indent=1)
print("DONE", len(results), "curves")
