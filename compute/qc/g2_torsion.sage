r"""Entry 131: are the known rational points of the three genus-2 D.odd curves torsion in the Jacobian?
For each non-Weierstrass known point P, the class [P - inf] reduces injectively mod good odd primes if it is
torsion, so its order in J(F_p) is then independent of p; differing orders prove infinite order (rank >= 1).
Equal orders n are confirmed exactly by n*D = 0 over Q.  Also the gcd of #J(F_p) (a torsion bound)."""
import json
CURVES = {"C_a": [25, -36, -18, 44, 1, 0], "C_b": [25, -4, -18, 12, 1, 0], "C_c": [1, -4, 6, 12, 1, 0]}
KNOWN = {"C_a": [(0, 0), (-1/5, 32/25), (-1, 0), (1, 4)], "C_b": [(0, 0), (-1/5, 16/25), (-1, 0), (1, 4)], "C_c": [(-1, 0), (0, 0), (1, 4)]}
out = {}
for name, cs in CURVES.items():
    R.<x> = QQ[]
    f = R(list(reversed(cs)))
    H = HyperellipticCurve(f)
    J = H.jacobian()
    disc = ZZ(f.discriminant())
    good = [p for p in prime_range(3, 60) if (disc * cs[0]) % p != 0]
    tors_bound = 0
    for p in good:
        tors_bound = gcd(tors_bound, H.change_ring(GF(p)).frobenius_polynomial()(1))
    rec = {"f": cs, "torsion_bound_gcd_JFp": int(tors_bound), "points": {}}
    for (px, py) in KNOWN[name]:
        P = H(QQ(px), QQ(py))
        if py == 0:
            rec["points"][str((px, py))] = "Weierstrass point: 2-torsion class"
            continue
        D = J(P)
        orders = {}
        for p in good[:8]:
            Hp = H.change_ring(GF(p)); Jp = Hp.jacobian()
            Dp = Jp(Hp(GF(p)(px), GF(p)(py)))
            Q = Dp; n = 1
            while not Q.is_zero() and n < 5000:
                Q = Q + Dp; n += 1
            orders[int(p)] = int(n)
        ns = set(orders.values())
        entry = {"orders_mod_p": orders}
        if len(ns) == 1:
            n = ns.pop()
            entry["exact_n_times_D_is_zero"] = bool((n * D).is_zero())
            entry["verdict"] = "torsion of order %d" % n if entry["exact_n_times_D_is_zero"] else "orders agree but n*D != 0 (?)"
        else:
            entry["verdict"] = "INFINITE ORDER (orders differ): rank >= 1"
        rec["points"][str((px, py))] = entry
        print(name, (px, py), entry, flush=True)
    print(name, "torsion bound", tors_bound, flush=True)
    out[name] = rec
json.dump(out, open("/home/will/qc_runs/g2_torsion_out.json", "w"), indent=1)
print("DONE")
