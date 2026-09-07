r"""Bielliptic quadratic Chabauty on G_delta: z^2 = delta (25 t^6 - 29 t^4 + 11 t^2 + 1) followed by
the first sieve step of [BP22, 4.2]: for every extra p-adic point, its coefficients modulo p^N in
J(Q)/tors with respect to B_1 = pi_1^*(G_1), B_2 = pi_2^*(G_2) (pushforwards [2 G_1, O] and
[O, 2 G_2]; a finite-index basis, whose index is a power of 2 and so invisible to p-adic
integrality for odd p).  A rational point has integral coefficients; an extra point with a
coefficient of negative valuation cannot be rational.  Usage: sage qc_coeff.sage delta p n N"""
import sys, json, time
load("/home/will/QC_bielliptic/qc_g2_bielliptic.sage")
d = ZZ(sys.argv[1]); p = ZZ(sys.argv[2]); n = ZZ(sys.argv[3]) if len(sys.argv) > 3 else 25; N = ZZ(sys.argv[4]) if len(sys.argv) > 4 else 4
R.<x> = QQ[]
f = d*(25*x^6 - 29*x^4 + 11*x^2 + 1)
a6, a4, a2, a0 = f[6], f[4], f[2], f[0]
H = HyperellipticCurve(f)
E1 = EllipticCurve([0, a4, 0, a2*a6, a0*a6^2]); E2 = EllipticCurve([0, a2, 0, a0*a4, a0^2*a6])
G1 = E1.gens()[0]; G2 = E2.gens()[0]
S1, i1, _ = E1.saturation([G1]); S2, i2, _ = E2.saturation([G2])
G1, G2 = S1[0], S2[0]
print("delta", d, "p", p, "n", n, "N", N, "| E1 gen", G1, "index", i1, "| E2 gen", G2, "index", i2, flush=True)
P1 = 2*G1; P2 = 2*G2
im_divisors = [[(P1[0], P1[1], 1), (0, 1, 0)], [(0, 1, 0), (P2[0], P2[1], 1)]]
base_pt = H(0, 1) if d == 1 else H(1, 4)
t0 = time.time()
rat, other = quadratic_chabauty_bielliptic(f, p, n, omega_info=True)
print("QC done in %.0fs; Omega size %d; rational per class %s; extra per class %s" % (time.time() - t0, len(rat), [len(L) for L in rat], [len(L) for L in other]), flush=True)
# coefficients of the recovered rational points (sanity: integral)
allrat = [P for L in rat for P in L]
def affine(P):
    if P[2] == 0:
        return "inf+" if P[0]*P[1] > 0 else "inf-"
    return P
sane = coefficients_mod_pN_v2(f, [affine(P) for P in allrat if affine(P) != base_pt], im_divisors, base_pt, p, N, k=5) if allrat else []
print("rational points' coefficients:", [(str(P), [str(c[0]), str(c[1])]) for P, c in zip([P for P in allrat if affine(P) != base_pt], sane)], flush=True)
summary = {"delta": int(d), "p": int(p), "n": int(n), "N": int(N), "omega_size": len(rat), "rational": [[str(P) for P in L] for L in rat],
           "classes": []}
for i, L in enumerate(other):
    rec = {"class": i, "n_extra": len(L), "n_integral": 0, "integral_coeffs": []}
    if L:
        try:
            cs = coefficients_mod_pN_v2(f, L, im_divisors, base_pt, p, N, k=5)
            if min(min(c[0].precision_absolute(), c[1].precision_absolute()) for c in cs) < N:
                cs = coefficients_mod_pN_v2(f, L, im_divisors, base_pt, p, N, k=10)
            for P, c in zip(L, cs):
                ok = c[0].valuation() >= 0 and c[1].valuation() >= 0
                if ok:
                    rec["n_integral"] += 1
                    rec["integral_coeffs"].append([int(ZZ(c[0])), int(ZZ(c[1])), str(P)])
        except Exception as e:
            rec["error"] = str(e)[:200]
    summary["classes"].append(rec)
    print("class %2d: extra %3d, with integral coefficients %3d %s" % (i, rec["n_extra"], rec["n_integral"], rec.get("error", "")), flush=True)
json.dump(summary, open("/home/will/qc_runs/coeff_d%d_p%d.json" % (int(d), int(p)), "w"), indent=1)
print("DONE delta", d, "p", p, "| classes with a surviving extra point:", sum(1 for r in summary["classes"] if r["n_integral"] > 0), "| surviving extra points:", sum(r["n_integral"] for r in summary["classes"]), flush=True)
