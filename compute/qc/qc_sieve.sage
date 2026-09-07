r"""The Mordell-Weil sieve for the bielliptic quadratic Chabauty output on
G_delta: z^2 = delta (25 t^6 - 29 t^4 + 11 t^2 + 1), run on E_1 x E_2 (no genus-2 Jacobian arithmetic).

Facts used.  E_1: y^2 = x^3 + a4 x^2 + a2 a6 x + a0 a6^2 and E_2: y^2 = x^3 + a2 x^2 + a0 a4 x + a0^2 a6
(the code's models) have rank 1, trivial torsion, saturated generators G_1, G_2; J(Q) is torsion-free
(gcd of #J(F_l) = 1); the quotient maps are pi_1(x, y) = (a6 x^2, a6 y) and pi_2(x, y) = (a0/x^2, a0 y/x^3),
with pi_1(inf+-) = O, pi_2(inf+-) = (0, +-a0 sqrt(a6)), pi_2((0, y)) = O.  For a rational point P of H
the QC code's coefficients (A, B) modulo p^N (w.r.t. B_1 = pi_1^* G_1, B_2 = pi_2^* G_2, pushforwards
[2 G_1, O] and [O, 2 G_2]) satisfy  pi_1(P) = pi_1(P_0) + 2A G_1,  pi_2(P) = pi_2(P_0) + 2B G_2  in E_i(Q),
so m_1 = 2A, m_2 = 2B are integers determined modulo p^N by the p-adic point.

The sieve.  For each Omega-class the candidates are the CRT combinations of the residues (m_1, m_2) of the
extra 11-adic and 13-adic points; a rational point not yet recognised would produce one of them.  For an
auxiliary prime l of good reduction, o_i = ord(G_i mod l) and T_l = {(r_1, r_2) : pi_1(P0) + r_1 G_1,
pi_2(P0) + r_2 G_2 is the image of a point of H(F_l)}.  A candidate (m_1, m_2) mod M survives l iff some
(r_1, r_2) in T_l has r_1 = m_1 mod gcd(M, o_1) and r_2 = m_2 mod gcd(M, o_2).  The recovered rational
points are controls: their exact (m_1, m_2) must survive every l.
Usage: sage qc_sieve.sage delta   (primes 11 and 13, N = 4, auxiliary primes to 400)."""
import sys, json, time
load("/home/will/QC_bielliptic/qc_g2_bielliptic.sage")
d = ZZ(sys.argv[1]); PR = [11, 13]; n = 25; N = 4; LMAX = 400
R.<x> = QQ[]
f = d*(25*x^6 - 29*x^4 + 11*x^2 + 1)
a6, a4, a2, a0 = f[6], f[4], f[2], f[0]
H = HyperellipticCurve(f)
E1 = EllipticCurve([0, a4, 0, a2*a6, a0*a6^2]); E2 = EllipticCurve([0, a2, 0, a0*a4, a0^2*a6])
G1 = E1.saturation([E1.gens()[0]])[0][0]; G2 = E2.saturation([E2.gens()[0]])[0][0]
assert E1.torsion_order() == 1 and E2.torsion_order() == 1 and E1.rank() == 1 and E2.rank() == 1
P0 = H(0, 1) if d == 1 else H(1, 4)
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
print("delta", d, "| E1", E1.conductor(), "G1", G1, "| E2", E2.conductor(), "G2", G2, "| P0", P0, "| pi(P0)", Q1, Q2, flush=True)
# torsion of J(Q): gcd of #J(F_l)
tors = 0
for l in prime_range(3, 60):
    if l in (2, 5, 23):
        continue
    tors = gcd(tors, HyperellipticCurve(f.change_ring(GF(l))).frobenius_polynomial()(1))
print("gcd of #J(F_l):", tors, flush=True)
assert tors == 1

# ---- quadratic Chabauty and the coefficients, per prime ----
cands = {}       # p -> {class index: set of (m1, m2) mod p^N}
rational = {}    # p -> {class index: [(P, m1, m2)]}
omega_sizes = {}
for p in PR:
    t0 = time.time()
    rat, other = quadratic_chabauty_bielliptic(f, p, n, omega_info=True)
    omega_sizes[p] = len(rat)
    if p == PR[0]:
        rat_lists = rat
    cands[p] = {}; rational[p] = {}
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
    for i, L in enumerate(rat):
        recs = []
        for P in L:
            Pa = ("inf+" if P[0]*P[1] > 0 else "inf-") if P[2] == 0 else P
            if Pa == P0:
                recs.append((str(P), 0, 0)); continue
            # exact integers: pi_1(P) - Q1 = m1 G1
            m1 = (pi1(P) - Q1).log(G1) if False else None
            recs.append((str(P), None, None))
        rational[p][i] = recs
    print("p =", p, "QC + coefficients in %.0fs; Omega %d; candidates per class %s" % (time.time() - t0, len(rat), [len(cands[p][i]) for i in range(len(rat))]), flush=True)
assert omega_sizes[PR[0]] == omega_sizes[PR[1]]
nO = omega_sizes[PR[0]]

# exact coefficients of the recovered rational points (controls): solve pi_i(P) - Q_i = m_i G_i by a small search
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

# ---- auxiliary primes: orders and the image set T_l ----
def dlog_F(Pt, G, o):
    Q = Pt.curve()(0)
    for r in range(o):
        if Q == Pt:
            return r
        Q = Q + G
    return None
aux = []
M = prod(p^N for p in PR)
for l in prime_range(3, LMAX):
    if l in (2, 5, 23) or l in PR:
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
            continue                       # no leverage against the p-adic residues
        Q1l = E1l(Q1); Q2l = E2l(Q2)
        Hl = HyperellipticCurve(fl)
        a6l, a0l = Fl(a6), Fl(a0)
        T = set()
        imgs = []
        for P in Hl.points():
            if P[2] == 0:
                continue
            xx, yy = Fl(P[0]), Fl(P[1])
            A1 = E1l(a6l*xx^2, a6l*yy)
            A2 = E2l(0) if xx == 0 else E2l(a0l/xx^2, a0l*yy/xx^3)
            imgs.append((A1, A2))
        # the two points at infinity (rational over F_l iff a6 is a square mod l)
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

# ---- the sieve ----
def survives(m1, m2, l, o1, o2, T):
    g1, g2 = gcd(M, o1), gcd(M, o2)
    R1 = [(m1 + k*g1) % o1 for k in range(o1 // g1)]
    R2 = [(m2 + k*g2) % o2 for k in range(o2 // g2)]
    return any((r1, r2) in T for r1 in R1 for r2 in R2)
def crt_pair(res):        # res: {p: (m1, m2) mod p^N}
    m1 = crt([res[p][0] for p in PR], [p^N for p in PR]); m2 = crt([res[p][1] for p in PR], [p^N for p in PR])
    return (m1 % M, m2 % M)
report = {"delta": int(d), "primes": PR, "N": int(N), "omega": int(nO), "aux": [(int(l), int(o1), int(o2), len(T)) for (l, o1, o2, T) in aux], "classes": [], "controls": []}
# controls: the known rational points must survive every auxiliary prime
for (Ps, m1, m2) in controls:
    if m1 is None or m2 is None:
        report["controls"].append((Ps, "dlog not found")); continue
    bad = [l for (l, o1, o2, T) in aux if not survives(m1 % M, m2 % M, l, o1, o2, T)]
    report["controls"].append((Ps, int(m1), int(m2), "OK" if not bad else "FAILS at " + str(bad)))
    print("control", Ps, (m1, m2), "OK" if not bad else "FAILS at " + str(bad), flush=True)
total_survivors = 0
for i in range(nO):
    S11, S13 = cands[PR[0]][i], cands[PR[1]][i]
    pairs = [crt_pair({PR[0]: a, PR[1]: b}) for a in S11 for b in S13]
    surv = []
    for (m1, m2) in pairs:
        killers = [l for (l, o1, o2, T) in aux if not survives(m1, m2, l, o1, o2, T)]
        if not killers:
            surv.append((int(m1), int(m2)))
    total_survivors += len(surv)
    report["classes"].append({"class": i, "n11": len(S11), "n13": len(S13), "n_pairs": len(pairs), "survivors": surv})
    print("class %2d: %2d x %2d = %3d candidate pairs, survivors %d" % (i, len(S11), len(S13), len(pairs), len(surv)), flush=True)
report["total_survivors"] = total_survivors
json.dump(report, open("/home/will/qc_runs/sieve_d%d.json" % int(d), "w"), indent=1, default=int)
print("DONE delta", d, "| total surviving candidate pairs:", total_survivors, "| if 0: G_delta(Q) is exactly the recovered rational points", flush=True)
