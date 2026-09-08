r"""Bielliptic quadratic Chabauty + the E1 x E2 Mordell-Weil sieve for a general even sextic y^2 = f(x),
f = a6 x^6 + a4 x^4 + a2 x^2 + a0 (entry 130; generalises qc_sieve.sage of entry 118).
Usage: sage qc_general.sage a6 a4 a2 a0 p1 p2 [x0 y0]   (primes of good ordinary reduction; base point optional)"""
import sys, json, time
load("/home/will/QC_bielliptic/qc_g2_bielliptic.sage")
a6, a4, a2, a0 = [ZZ(v) for v in sys.argv[1:5]]
PR = [ZZ(sys.argv[5]), ZZ(sys.argv[6])]
n = 25; N = 4; LMAX = 400
R.<x> = QQ[]
f = a6*x^6 + a4*x^4 + a2*x^2 + a0
H = HyperellipticCurve(f)
E1 = EllipticCurve([0, a4, 0, a2*a6, a0*a6^2]); E2 = EllipticCurve([0, a2, 0, a0*a4, a0^2*a6])
print("f =", f, "| E1", E1.cremona_label(), "rank", E1.rank(), "tors", E1.torsion_order(), "| E2", E2.cremona_label(), "rank", E2.rank(), "tors", E2.torsion_order(), flush=True)
assert E1.rank() == 1 and E2.rank() == 1 and E1.torsion_order() == 1 and E2.torsion_order() == 1
for p in PR:
    assert E1.has_good_reduction(p) and E2.has_good_reduction(p) and E1.is_ordinary(p) and E2.is_ordinary(p), ("bad or supersingular prime", p)
G1 = E1.saturation([E1.gens()[0]])[0][0]; G2 = E2.saturation([E2.gens()[0]])[0][0]
if len(sys.argv) > 8:
    P0 = H(QQ(sys.argv[7]), QQ(sys.argv[8]))
else:
    P0 = next(P for P in H.rational_points(bound=30) if P[2] != 0)
im_divisors = [[((2*G1)[0], (2*G1)[1], 1), (0, 1, 0)], [(0, 1, 0), ((2*G2)[0], (2*G2)[1], 1)]]
def pi1(P):
    if P[2] == 0:
        return E1(0)
    return E1(a6*P[0]^2, a6*P[1])
def pi2(P):
    if P[2] == 0:
        s = sqrt(QQ(a6)); return E2(0, a0*s) if P[1]*P[0] > 0 else E2(0, -a0*s)
    if P[0] == 0:
        return E2(0)
    return E2(a0/P[0]^2, a0*P[1]/P[0]^3)
Q1, Q2 = pi1(P0), pi2(P0)
print("base point", P0, "| pi(P0)", Q1, Q2, "| G1", G1, "| G2", G2, flush=True)
tors = 0
for l in prime_range(3, 60):
    if f.change_ring(GF(l)).discriminant() == 0 or l in PR:
        continue
    tors = gcd(tors, HyperellipticCurve(f.change_ring(GF(l))).frobenius_polynomial()(1))
print("gcd of #J(F_l):", tors, flush=True)
assert tors == 1
cands = {}; omega_sizes = {}; rat_lists = None
for p in PR:
    t0 = time.time()
    rat, other = quadratic_chabauty_bielliptic(f, p, n, omega_info=True, potential_good_primes=False)     # the shortcut at primes of potential good reduction fails on Sage 10.7
    omega_sizes[p] = len(rat)
    if rat_lists is None:
        rat_lists = rat
    cands[p] = {}
    for i, L in enumerate(other):
        S = set()
        if L:
            cs = coefficients_mod_pN_v2(f, L, im_divisors, P0, p, N, k=5)
            if min(min(c[0].precision_absolute(), c[1].precision_absolute()) for c in cs) < N:
                cs = coefficients_mod_pN_v2(f, L, im_divisors, P0, p, N, k=10)
            for c in cs:
                assert c[0].valuation() >= 0 and c[1].valuation() >= 0
                S.add((ZZ(2*c[0]) % p^N, ZZ(2*c[1]) % p^N))
        cands[p][i] = S
    print("p =", p, "QC + coefficients in %.0fs; Omega %d; rational per class %s; candidates per class %s" % (time.time() - t0, len(rat), [len(L) for L in rat], [len(cands[p][i]) for i in range(len(rat))]), flush=True)
assert omega_sizes[PR[0]] == omega_sizes[PR[1]]
nO = omega_sizes[PR[0]]
def dlog_Q(Pt, G, bound=60):
    for m in range(-bound, bound + 1):
        if Pt == m*G:
            return m
    return None
ctrl_pts = []
for i in range(nO):
    for P in rat_lists[i]:
        if P[2] == 0:
            for sg in (1, -1):
                ctrl_pts.append(("inf" + ("+" if sg > 0 else "-"), E1(0), E2(0, sg*a0*sqrt(QQ(a6)))))
        else:
            ctrl_pts.append((str(P), pi1(P), pi2(P)))
controls = [(lab, dlog_Q(A1 - Q1, G1), dlog_Q(A2 - Q2, G2)) for (lab, A1, A2) in ctrl_pts]
print("recovered rational points and their (m1, m2):", controls, flush=True)
def dlog_F(Pt, G, o):
    Q = Pt.curve()(0)
    for r in range(o):
        if Q == Pt:
            return r
        Q = Q + G
    return None
aux = []
M = prod(p^N for p in PR)
bad = set(ZZ(f.discriminant()).prime_divisors()) | set(PR) | {2}
for l in prime_range(3, LMAX):
    if l in bad:
        continue
    Fl = GF(l)
    try:
        E1l = E1.change_ring(Fl); E2l = E2.change_ring(Fl)
        if not (E1.has_good_reduction(l) and E2.has_good_reduction(l)):
            continue
        fl = f.change_ring(Fl)
        if fl.discriminant() == 0:
            continue
        G1l = E1l(G1); G2l = E2l(G2); o1 = G1l.order(); o2 = G2l.order()
        if gcd(M, o1) == 1 and gcd(M, o2) == 1:
            continue
        Q1l = E1l(Q1); Q2l = E2l(Q2)
        Hl = HyperellipticCurve(fl)
        a6l, a0l = Fl(a6), Fl(a0)
        T = set(); imgs = []
        for P in Hl.points():
            if P[2] == 0:
                continue
            xx, yy = Fl(P[0]), Fl(P[1])
            A1 = E1l(a6l*xx^2, a6l*yy)
            A2 = E2l(0) if xx == 0 else E2l(a0l/xx^2, a0l*yy/xx^3)
            imgs.append((A1, A2))
        if a6l.is_square():
            s = a6l.sqrt()
            for sg in (1, -1):
                imgs.append((E1l(0), E2l(0, sg*a0l*s)))
        for (A1, A2) in imgs:
            r1 = dlog_F(A1 - Q1l, G1l, o1); r2 = dlog_F(A2 - Q2l, G2l, o2)
            if r1 is not None and r2 is not None:
                T.add((r1, r2))
        aux.append((l, o1, o2, T))
    except Exception as e:
        print("  l =", l, "skipped:", str(e)[:80], flush=True)
print("auxiliary primes with leverage:", [(l, o1, o2, len(T)) for (l, o1, o2, T) in aux], flush=True)
def survives(m1, m2, l, o1, o2, T):
    g1, g2 = gcd(M, o1), gcd(M, o2)
    R1 = [(m1 + k*g1) % o1 for k in range(o1 // g1)]
    R2 = [(m2 + k*g2) % o2 for k in range(o2 // g2)]
    return any((r1, r2) in T for r1 in R1 for r2 in R2)
def crt_pair(res):
    m1 = crt([res[p][0] for p in PR], [p^N for p in PR]); m2 = crt([res[p][1] for p in PR], [p^N for p in PR])
    return (m1 % M, m2 % M)
report = {"f": [int(a6), int(a4), int(a2), int(a0)], "E1": E1.cremona_label(), "E2": E2.cremona_label(), "primes": [int(p) for p in PR], "N": int(N), "omega": int(nO),
          "base_point": str(P0), "rational_points": [[str(P) for P in L] for L in rat_lists],
          "aux": [(int(l), int(o1), int(o2), len(T)) for (l, o1, o2, T) in aux], "classes": [], "controls": []}
for (Ps, m1, m2) in controls:
    if m1 is None or m2 is None:
        report["controls"].append((Ps, "dlog not found")); continue
    bad_l = [l for (l, o1, o2, T) in aux if not survives(m1 % M, m2 % M, l, o1, o2, T)]
    report["controls"].append((Ps, int(m1), int(m2), "OK" if not bad_l else "FAILS at " + str(bad_l)))
    print("control", Ps, (m1, m2), "OK" if not bad_l else "FAILS at " + str(bad_l), flush=True)
total = 0
for i in range(nO):
    S1, S2 = cands[PR[0]][i], cands[PR[1]][i]
    pairs = [crt_pair({PR[0]: a, PR[1]: b}) for a in S1 for b in S2]
    surv = [(int(m1), int(m2)) for (m1, m2) in pairs if not [l for (l, o1, o2, T) in aux if not survives(m1, m2, l, o1, o2, T)]]
    total += len(surv)
    report["classes"].append({"class": i, "n1": len(S1), "n2": len(S2), "n_pairs": len(pairs), "survivors": surv})
    print("class %2d: %2d x %2d = %3d candidate pairs, survivors %d" % (i, len(S1), len(S2), len(pairs), len(surv)), flush=True)
report["total_survivors"] = total
tag = "_".join(str(v) for v in (a6, a4, a2, a0))
json.dump(report, open("/home/will/qc_runs/general_%s.json" % tag, "w"), indent=1, default=int)
print("DONE f =", f, "| total surviving candidate pairs:", total, "| if 0: H(Q) is exactly the recovered rational points", flush=True)
