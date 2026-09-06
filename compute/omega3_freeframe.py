"""THE FREE-FRAME REDUCTION (entry 116): the first instance of goal G, omega = 3 -> omega = 2.

A class of a three-frame box in which some frame f appears in exactly ONE label L is a
"free-frame class".  The element e(L) is the only place f enters, so:

 * if L is C (resp. D), the relation R2 = eA e(A) - eB e(B) - eD e(D) (resp. R1) does not
   contain e(L) at all: it is a signed THREE-TERM additive relation among elements of the
   two-frame box of the remaining frames -- and the ladder theorems say no such relation has
   a solution in frames of two distinct split primes: A3.7 for shape (1,1), A3.8 for (2,1),
   A3.9 for (3,1), A3.10 for (2,2).  The class is DEAD by theorem (kill 'T').
 * if L is A or B, eliminating e(L) between the relations leaves the WEIGHTED relation
   2 eB e(B) - eC e(C) + eD e(D) = 0 (resp. 2 eA e(A) - ...), a four-term relation with a
   doubled element, outside the ladder's literal scope.  Then, with the third frame reduced
   to its norm, G(t_g, t_h) = 0 is a polynomial relation of the two frame ratios:
     - a factor that is a torsion coset w_g^a w_h^b = zeta in the torus coordinates cannot
       hold for frames of distinct primes (Lemma B, entry 111): kill 'B';
     - a factor linear in t_g gives t_g = P(t_h)/Q(t_h), and t_g is a frame ratio only if
       P^2 + Q^2 is a square: the FRAME-CONDITION CURVE y^2 = P^2 + Q^2 (the killers of
       entry 112 are exactly these curves).  Genus 1 and rank 0: its torsion points are
       enumerated completely (PARI ellrank / elltors / hyperellratpoints), each gives a pair
       (t_g, t_h), and an admissible pair must still lift to the free frame (e(L) is then
       determined and t_f must be a rational frame-ratio root): kill 'E' when none lifts;
     - a reduced relation that is a product of norms and monomials holds only at degenerate
       frames: kill 'Z'.
Everything else is 'undecided' (higher-genus frame conditions, relations not linear in
either frame).  The verdicts are exact; the elliptic route depends on PARI's rank 0 being
certified (ellrank's upper bound 0) and the point list being complete (torsion order)."""
from __future__ import annotations
import re, subprocess
import sympy as sp
from compute import omega3 as O
from compute.omega3 import is_frame_ratio, degenerate
from compute.pari_genus1 import GP

T = sp.Symbol("T_ff"); X = sp.Symbol("X_ff")
wg, wh = sp.symbols("w_g w_h")
LADDER = {(1, 1): "A3.7", (2, 1): "A3.8", (1, 2): "A3.8", (3, 1): "A3.9", (1, 3): "A3.9", (2, 2): "A3.10"}


def _gp(script, timeout=300):
    return subprocess.run([GP, "-q"], input=script + "\nquit\n", capture_output=True, text=True, timeout=timeout).stdout


def free_frame(cand):
    """(f, w): the frame f appearing in exactly one label and the index w of that label, or None."""
    labs = cand[:4]
    counts = [sum(1 for lab in labs if lab[f] != 0) for f in range(3)]
    if 1 not in counts:
        return None
    f = counts.index(1)
    return f, [i for i, lab in enumerate(labs) if lab[f] != 0][0]


def two_frame_shape(cand, f):
    g, h = [i for i in range(3) if i != f]
    return (max(abs(lab[g]) for lab in cand[:4]), max(abs(lab[h]) for lab in cand[:4])), (g, h)


def reduced_relation(cand, f, w):
    """The relation free of the free element: coef2 R1 - coef1 R2 (R2 itself for L = C, R1 for L = D)."""
    R1, R2 = O.relations(cand)
    A, B, C, D, eA, eB, eC, eD = cand
    coef1 = [eA, eB, -eC, 0][w]; coef2 = [eA, -eB, 0, -eD][w]
    return sp.expand(coef2 * R1 - coef1 * R2)


def main_factors(red, f):
    """The factors of the reduced relation in ratio form (tg, th), dropping the free frame's norm,
    pure norms, monomials and constants; None if the free frame's angle survives."""
    g, h = [i for i in range(3) if i != f]
    (cg, sg), (ch, sh) = O.FR[g], O.FR[h]
    out = []
    for q, m in sp.factor_list(red)[1]:
        fs = q.free_symbols
        if not fs or fs <= set(O.FR[f]):
            continue
        if q in (cg, sg, ch, sh) or sp.expand(q - (cg ** 2 + sg ** 2)) == 0 or sp.expand(q - (ch ** 2 + sh ** 2)) == 0:
            continue
        if fs & set(O.FR[f]):
            return None
        Gt = sp.expand(q.subs({sg: O.tg * cg, sh: O.th * ch}, simultaneous=True))
        Gt = sp.expand(sp.Mul(*[qq ** mm for qq, mm in sp.factor_list(Gt)[1] if qq.free_symbols & {O.tg, O.th}]))
        out.append(Gt)
    return out


def coset_factor(Gt):
    """{'a', 'b', 'zeta', 'order'} if Gt(tg, th) is, in the torus coordinates and up to the unit
    factors (w + 1), a binomial w_g^a w_h^b - zeta with zeta a root of unity; else None."""
    sub = {O.tg: -sp.I * (wg - 1) / (wg + 1), O.th: -sp.I * (wh - 1) / (wh + 1)}
    P = sp.Poly(sp.expand(sp.numer(sp.together(Gt.subs(sub)))), wg, wh)
    for var in (wg, wh):
        while True:
            q, r = sp.div(P, sp.Poly(var + 1, wg, wh))
            if r.is_zero:
                P = q
            else:
                break
    terms = P.terms()
    if len(terms) != 2:
        return None
    (m1, c1), (m2, c2) = terms
    a, b = m1[0] - m2[0], m1[1] - m2[1]
    if (a, b) == (0, 0):
        return None
    z = sp.simplify(-c2 / c1)
    if sp.simplify(sp.Abs(z) - 1) != 0:
        return None
    for n in (1, 2, 4, 8, 12):
        if sp.simplify(z ** n - 1) == 0:
            return {"a": int(a), "b": int(b), "zeta": str(z), "order": n}
    return None


def quartic_data(fpoly):
    """y^2 = fpoly(T) (degree 3 or 4): PARI rank bounds, torsion order, label, affine points to
    10^5, points at infinity, and whether the list is complete (rank 0 and #points = torsion)."""
    coeffs = [int(v) for v in sp.Poly(fpoly, T).all_coeffs()]
    lc = coeffs[0]
    n_inf = 2 if (len(coeffs) == 5 and lc > 0 and sp.sqrt(sp.Integer(lc)).is_Integer) else (1 if len(coeffs) == 4 else 0)
    out = _gp("f = Pol(" + str(coeffs) + "); E = ellinit(ellfromeqn(y^2 - f)); r = ellrank(E); Tt = elltors(E); id = ellidentify(E);"
              "print(\"RES \", r[1], \" \", r[2], \" \", Tt[1], \" \", id[1][1]); print(\"PTS \", hyperellratpoints(f, 100000));")
    m = re.search(r"RES (\d+) (\d+) (\d+) (\S+)", out); p = re.search(r"PTS \[(.*)\]", out, re.S)
    if not m:
        return {"error": out[-200:]}
    pts = [(sp.Rational(a), sp.Rational(b)) for a, b in re.findall(r"\[([^\[\],]+), ([^\[\],]+)\]", p.group(1))] if p else []
    return {"rank_lower": int(m.group(1)), "rank_upper": int(m.group(2)), "torsion": int(m.group(3)), "label": m.group(4),
            "affine_points": pts, "n_infinity": n_inf, "complete": int(m.group(2)) == 0 and len(pts) + n_inf == int(m.group(3))}


def lift_ok(cand, f, tg_v, th_v):
    """Can the free frame be admissible over the pair?  The pair substituted into R1 and R2 leaves
    polynomials in the free frame's ratio; a common rational root that is a frame ratio is needed."""
    g, h = [i for i in range(3) if i != f]
    (cg, sg), (ch, sh), (cf, sf) = O.FR[g], O.FR[h], O.FR[f]
    roots = None
    for R in O.relations(cand):
        P = sp.expand(R.subs({cg: 1, sg: tg_v, ch: 1, sh: th_v, cf: 1, sf: X}))
        if P == 0:
            continue
        rs = {r for r in sp.Poly(P, X).ground_roots() if r.is_rational}
        roots = rs if roots is None else roots & rs
    if roots is None:
        return True, "both relations vanish identically"
    adm = [r for r in roots if not degenerate(r) and is_frame_ratio(r)]
    return bool(adm), [str(r) for r in adm]


def decide(cand, box=None):
    """The free-frame verdict of a class: {'status': 'DEAD' | 'undecided' | 'no free frame' | ...,
    'kill': ..., 'factors': [...]}.  Kills: 'T' (ladder theorem), 'Z' (degenerate-only relation),
    'B' (torsion coset), 'E' (elliptic frame condition of rank 0 with degenerate or unliftable points)."""
    if box is not None:
        O.set_box(box)
    cand = tuple(tuple(x) if isinstance(x, list) else x for x in cand)
    ff = free_frame(cand)
    if ff is None:
        return {"cand": cand, "status": "no free frame"}
    f, w = ff
    rec = {"cand": cand, "free_frame": f, "label": "ABCD"[w], "status": None}
    if w in (2, 3):
        shape, _ = two_frame_shape(cand, f)
        thm = LADDER.get(shape)
        if thm:
            rec.update({"status": "DEAD", "kill": "T", "theorem": thm, "shape": list(shape)}); return rec
        rec["note"] = "two-frame shape " + str(shape) + " has no ladder theorem"
    red = reduced_relation(cand, f, w)
    if red == 0:
        rec["status"] = "reduced relation vanishes"; return rec
    facs = main_factors(red, f)
    if facs is None:
        rec["status"] = "free frame survives"; return rec
    if not facs:
        rec.update({"status": "DEAD", "kill": "Z", "reduced": str(sp.factor(red))[:200]}); return rec
    rec["factors"] = []; all_dead = True
    for Gt in facs:
        fr = {"G": str(Gt)}
        cf = coset_factor(Gt)
        if cf:
            fr.update({"kill": "B", "coset": cf}); rec["factors"].append(fr); continue
        Pq = sp.Poly(Gt, O.tg, O.th); dg, dh = Pq.degree(O.tg), Pq.degree(O.th)
        fr["degrees"] = [dg, dh]
        if dg == 1:
            solve_var, other = O.tg, O.th
        elif dh == 1:
            solve_var, other = O.th, O.tg
        else:
            fr["status"] = "not linear in either frame"; rec["factors"].append(fr); all_dead = False; continue
        Pl = sp.Poly(Gt, solve_var); G1, G0 = Pl.all_coeffs()
        Pn, Qd = sp.expand(-G0.subs(other, T)), sp.expand(G1.subs(other, T))
        gcd = sp.gcd(Pn, Qd); Pn, Qd = sp.cancel(Pn / gcd), sp.cancel(Qd / gcd)
        Fc = sp.expand(Pn ** 2 + Qd ** 2)
        sqf = sp.factor_list(Fc); Fs = sp.Integer(sqf[0])
        for q, m in sqf[1]:
            Fs *= q ** (m % 2)
        Fs = sp.expand(Fs)
        deg = sp.Poly(Fs, T).degree() if Fs.free_symbols else 0
        genus = (deg - 1) // 2 if deg % 2 else max(deg // 2 - 1, 0)
        fr.update({"solved": str(solve_var), "P": str(Pn), "Q": str(Qd), "frame_condition": str(Fs), "deg": deg, "genus": genus})
        if deg == 0:
            fr["status"] = "constant frame condition (" + ("square" if sp.sqrt(Fs).is_Rational else "not a square") + ")"
            if not sp.sqrt(Fs).is_Rational:
                fr["kill"] = "Z"
            else:
                all_dead = False
            rec["factors"].append(fr); continue
        if genus != 1:
            fr["status"] = "genus " + str(genus) + " frame condition"; rec["factors"].append(fr); all_dead = False; continue
        qd = quartic_data(Fs)
        fr["curve"] = {k: (v if k != "affine_points" else [(str(a), str(b)) for a, b in v]) for k, v in qd.items()}
        if qd.get("error") or not qd["complete"]:
            fr["status"] = "elliptic, rank bound " + str(qd.get("rank_upper")) + " (" + str(qd.get("label")) + ")"; rec["factors"].append(fr); all_dead = False; continue
        pairs = []
        for Tv in sorted({a for a, b in qd["affine_points"]}, key=float):
            Qv = Qd.subs(T, Tv)
            pairs.append((sp.oo if Qv == 0 else Pn.subs(T, Tv) / Qv, Tv))
        if qd["n_infinity"]:
            dP, dQ = sp.Poly(Pn, T).degree(), sp.Poly(Qd, T).degree()
            pairs.append((sp.oo if dP > dQ else (sp.Rational(sp.Poly(Pn, T).LC(), sp.Poly(Qd, T).LC()) if dP == dQ else sp.Integer(0)), sp.oo))
        cands = []
        for sv, ov in pairs:
            if sv in (sp.oo, sp.zoo) or ov == sp.oo or degenerate(sv) or degenerate(ov) or not is_frame_ratio(sv) or not is_frame_ratio(ov):
                cands.append({"solved": str(sv), "other": str(ov), "admissible": False}); continue
            tg_v, th_v = (sv, ov) if solve_var == O.tg else (ov, sv)
            ok, info = lift_ok(cand, f, tg_v, th_v)
            cands.append({"solved": str(sv), "other": str(ov), "admissible": True, "liftable": ok, "lift": info})
            if ok:
                all_dead = False
        fr["candidates"] = cands
        fr["kill"] = "E" if not any(c.get("liftable") for c in cands) else None
        fr["status"] = "rank 0 (" + qd["label"] + "), torsion " + str(qd["torsion"]) + (": dead" if fr["kill"] else ": a liftable admissible pair")
        rec["factors"].append(fr)
    if all(fr.get("kill") for fr in rec["factors"]) and all_dead:
        rec["status"] = "DEAD"; rec["kill"] = "".join(sorted({fr["kill"] for fr in rec["factors"]}))
    else:
        rec["status"] = "undecided"
    return rec
