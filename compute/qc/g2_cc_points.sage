r"""Entry 131: the rational points of C_c: y^2 = x^5 - 4x^4 + 6x^3 + 12x^2 + x, given that J(Q) has rank 0
(LMFDB 1408.b.180224.2, rank 0 proved by 2-descent; C_c is Q-isomorphic to it via x -> (x - 1)/(-x - 1), y -> 2y/(-x-1)^3).
With rank 0, J(Q) is torsion; the gcd of #J(F_p) over good odd primes bounds its order by 16, and the classes of the known
points generate a group of order 16, so J(Q) = <D, T> with D = [(1,4) - inf] of order 8 and T = [(0,0) - inf] (order 2).
C(Q) embeds in J(Q) by P -> [P - inf]; a class is of that form iff its reduced Mumford representative (u, v) has deg u <= 1;
enumerating the 16 classes gives C_c(Q) exactly."""
import json
R.<x> = QQ[]
f = x^5 - 4*x^4 + 6*x^3 + 12*x^2 + x
H = HyperellipticCurve(f); J = H.jacobian()
D = J(H(1, 4)); T1 = J(H(0, 0)); T2 = J(H(-1, 0))
assert (8*D).is_zero() and not (4*D).is_zero() and (2*T1).is_zero() and (2*T2).is_zero()
print("4D =", 4*D, "| T1 =", T1, "| T2 =", T2, "| T1+T2 =", T1 + T2)
T = T2 if any(str(k*D) == str(T1) for k in range(8)) else T1
print("T1 in <D>:", any(str(k*D) == str(T1) for k in range(8)), "| T2 in <D>:", any(str(k*D) == str(T2) for k in range(8)))
classes = {}
for k in range(8):
    for e in range(2):
        C = k*D + e*T
        key = str(C)
        classes[key] = (k, e)
print("distinct classes among k*D + e*T:", len(classes))
assert len(classes) == 16
# also T2 must be among them (J(Q) has order exactly 16)
assert str(T1) in classes and str(T2) in classes and str(T1 + T2) in classes
pts = []
for key, (k, e) in classes.items():
    C = k*D + e*T
    u, v = C[0], C[1]
    if u.degree() == 0:
        pts.append(("inf", (k, e)))
    elif u.degree() == 1:
        x0 = -u[0] / u[1]
        y0 = v(x0)
        assert y0^2 == f(x0)
        pts.append(((x0, y0), (k, e)))
print("C_c(Q) =", pts)
disc = ZZ(f.discriminant())
tb = 0
for p in prime_range(3, 100):
    if disc % p:
        tb = gcd(tb, H.change_ring(GF(p)).frobenius_polynomial()(1))
print("torsion bound gcd #J(F_p), p < 100:", tb)
json.dump({"f": [1, -4, 6, 12, 1, 0], "torsion_bound": int(tb), "n_classes": 16,
           "points": [str(P) for P, _ in pts], "classes_of_points": {str(P): list(ke) for P, ke in pts}},
          open("/home/will/qc_runs/g2_cc_points.json", "w"), indent=1)
print("DONE")

