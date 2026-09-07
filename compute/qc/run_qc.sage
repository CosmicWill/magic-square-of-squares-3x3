import sys, json, time
load("/home/will/QC_bielliptic/qc_g2_bielliptic.sage")
d = ZZ(sys.argv[1]); p = ZZ(sys.argv[2]); n = ZZ(sys.argv[3]) if len(sys.argv) > 3 else 25
R.<x> = QQ[]
f = d*(25*x^6 - 29*x^4 + 11*x^2 + 1)
t0 = time.time()
print("delta", d, "p", p, "n", n, "f =", f, flush=True)
rat, other = quadratic_chabauty_bielliptic(f, p, n, omega_info=True)
el = time.time() - t0
print("RATIONAL POINTS (per Omega element):", [[str(P) for P in L] for L in rat], flush=True)
print("EXTRA p-adic points per Omega element:", [len(L) for L in other], flush=True)
for i, L in enumerate(other):
    for P in L[:6]:
        print("   extra[%d]:" % i, P, flush=True)
json.dump({"delta": int(d), "p": int(p), "n": int(n), "rational_points": [[str(P) for P in L] for L in rat], "n_extra": [len(L) for L in other],
           "extra": [[str(P) for P in L] for L in other], "seconds": el},
          open("/home/will/qc_runs/qc_d%d_p%d.json" % (d, p), "w"), indent=1)
print("DONE delta", d, "p", p, "in %.0fs" % el, flush=True)
