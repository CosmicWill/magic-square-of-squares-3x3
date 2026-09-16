# The Prym test without Magma (entry 142).  For a route-less family (A, B, C, D of compute/data_prym_test_142.json) and primes p:
# the L-polynomial of the full quotient Gamma/G (genus 3 or 4) from the numbers of places of degree <= g of its function field
# over GF(p) (Newton's identities + the functional equation), and for each index-2 quotient Gamma/H the L-polynomial of the Prym
# part P = J(Gamma/H) / J(Gamma/G) from the places of degree <= dim P = g(Gamma/H) - g(Gamma/G) alone (the power sums of the
# Frobenius eigenvalues of J(Gamma/H) minus those of J(Gamma/G); Kani-Rosen: J(Gamma/H) ~ J(Gamma/G) x P over the base field, so
# the L-polynomials multiply).  Checks: the genus of the reduction equals the genus over Q (then the Jacobian has good reduction
# at p and the counts are those of its reduction), the exact constant field is GF(p), the coefficients are integers and the
# reciprocal roots have absolute value sqrt(p) (Weil).  With "validate": the full L-polynomial of each index-2 quotient (places
# up to its genus) is compared with the product L(Gamma/G) L(P).
# Usage (from the repository root, SageMath >= 10):  sage compute/qc/prym_test.sage A 5 13 [validate] [out=FILE]
# Results are merged into FILE (default prym_test_<family>.json in the working directory); the records of
# compute/data_prym_test_142.json were produced by this code (scratch version prym_count.sage, 2026-09-15).
import json, re, sys, time, os
args = sys.argv[1:]
fams = [a for a in args if a in ("A", "B", "C", "D")] or ["A", "B", "C", "D"]
primes = [int(a) for a in args if a.isdigit()] or [5, 7, 11, 13, 3]
validate = "validate" in args
outs = [a[4:] for a in args if a.startswith("out=")]
data_path = [a[5:] for a in args if a.startswith("data=")]
data_path = data_path[0] if data_path else os.path.join("compute", "data_prym_test_142.json")
T = json.load(open(data_path))
INTS = ["joint", "diag(1,1)", "diag(-1,-1)"]


def build(fstr, p):
    """The function field over GF(p) of the plane curve fstr (two variables; the one of smaller degree is the extension variable)."""
    syms = sorted(set(re.findall(r"[A-Za-z][A-Za-z0-9]*", fstr)))
    assert len(syms) == 2, syms
    Rz = PolynomialRing(ZZ, syms)
    Fz = Rz(fstr.replace("**", "^"))
    degs = [Fz.degree(v) for v in Rz.gens()]
    ext, base = (syms[0], syms[1]) if degs[0] <= degs[1] else (syms[1], syms[0])
    K = FunctionField(GF(p), 'x')
    x = K.gen()
    R = PolynomialRing(K, 'y')
    y = R.gen()
    F = R(eval(fstr, {"__builtins__": {}}, {base: x, ext: y}))
    if F.degree() < 1:
        return None, "degree 0 in the extension variable mod %d" % p
    if not F.is_irreducible():
        return None, "reducible mod %d" % p
    L = K.extension(F, names=('yy',))
    return L, None


def power_sums_from_L(a, kmax):
    """a = coefficients of L(t) = prod (1 - alpha t); returns [s_1..s_kmax], s_k = sum alpha^k."""
    s = []
    for i in range(1, kmax + 1):
        ai = a[i] if i < len(a) else 0
        si = -i * ai - sum(s[j - 1] * (a[i - j] if i - j < len(a) else 0) for j in range(1, i))
        s.append(si)
    return s


def L_from_power_sums(s, d, q):
    """s = [s_1..s_d] of a 2d-dimensional Weil polynomial; returns its coefficients a_0..a_{2d} via Newton + the functional equation."""
    a = [QQ(1)]
    for i in range(1, d + 1):
        a.append(-sum(s[j - 1] * a[i - j] for j in range(1, i + 1)) / i)
    for i in range(d + 1, 2 * d + 1):
        a.append(QQ(q) ** (i - d) * a[2 * d - i])
    return a


def weil_ok(a, q):
    Tt = PolynomialRing(QQ, 't')
    P = Tt(a)
    if any(c not in ZZ for c in a):
        return False, "non-integral coefficients"
    roots = P.roots(CC, multiplicities=True)
    if sum(m for _, m in roots) != P.degree():
        return False, "root count"
    bad = [r for r, _ in roots if abs(abs(r) - 1 / sqrt(RR(q))) > 1e-6]
    return (not bad), ("%d reciprocal roots off sqrt(q)" % len(bad) if bad else "ok")


def factor_degrees(a):
    Tt = PolynomialRing(ZZ, 't')
    P = Tt([ZZ(c) for c in a])
    return sorted([(int(f.degree()), int(e)) for f, e in P.factor()]), str(P)


for fam in fams:
    F = T["families"][fam]
    rec, gfam = F["curves"], F["genera"]
    outfile = outs[0] if outs else "prym_test_%s.json" % fam
    out = json.load(open(outfile)) if os.path.exists(outfile) else {"family": fam, "index": F["representative"]["index"], "frame": F["representative"]["frame"], "members": F["members"], "genera": gfam, "primes": {}}
    for p in primes:
        t0 = time.time()
        res = {"p": p, "curves": {}}
        print("== family", fam, "p =", p, flush=True)
        L, err = build(rec["full"], p)
        gfull = gfam["full"]
        if err is None:
            gred = int(L.genus())
            E, _ = L.exact_constant_field()
            cdeg = int(E.degree())
            if gred != gfull or cdeg != 1:
                err = "full: genus of the reduction %d (over Q %d), exact constant field degree %d" % (gred, gfull, cdeg)
        if err is not None:
            res["bad"] = err
            print("   ", err, flush=True)
            out["primes"][str(p)] = res
            json.dump(out, open(outfile, "w"), indent=1)
            continue
        t1 = time.time()
        Bfull = [len(L.places(d)) for d in range(1, gfull + 1)]
        Nfull = [sum(e * Bfull[e - 1] for e in ZZ(k).divisors()) for k in range(1, gfull + 1)]
        sfull = [p ** k + 1 - Nfull[k - 1] for k in range(1, gfull + 1)]
        afull = L_from_power_sums(sfull, gfull, p)
        sage_L = list(L.L_polynomial())
        ok, why = weil_ok(afull, p)
        fd, fstr = factor_degrees(afull)
        res["curves"]["full"] = {"genus": gfull, "places_by_degree": Bfull, "N": [int(n) for n in Nfull], "L": [int(c) for c in afull], "L_str": fstr, "factor_degrees": fd,
                                "weil": why, "matches_sage_L_polynomial": [int(c) for c in sage_L] == [int(c) for c in afull], "seconds": float("%.1f" % (time.time() - t1))}
        print("    full: genus", gfull, "| L factor degrees", fd, "| weil", why, "| Sage agrees", res["curves"]["full"]["matches_sage_L_polynomial"], "| %.0fs" % (time.time() - t1), flush=True)
        for kind in INTS:
            t1 = time.time()
            Li, err = build(rec[kind], p)
            gi = gfam[kind]
            d = gi - gfull
            if err is None:
                gred = int(Li.genus())
                E, _ = Li.exact_constant_field()
                cdeg = int(E.degree())
                if gred != gi or cdeg != 1:
                    err = "genus of the reduction %d (over Q %d), exact constant field degree %d" % (gred, gi, cdeg)
            if err is not None:
                res["curves"][kind] = {"bad": err}
                print("   ", kind, ":", err, flush=True)
                continue
            B = [len(Li.places(e)) for e in range(1, d + 1)]
            N = [sum(e * B[e - 1] for e in ZZ(k).divisors()) for k in range(1, d + 1)]
            s = [p ** k + 1 - N[k - 1] for k in range(1, d + 1)]
            sf = power_sums_from_L(afull, d)
            sP = [s[k] - sf[k] for k in range(d)]
            aP = L_from_power_sums(sP, d, p)
            ok, why = weil_ok(aP, p)
            entry = {"genus": gi, "dim_prym": d, "places_by_degree": B, "N": [int(n) for n in N], "weil": why, "seconds": float("%.1f" % (time.time() - t1))}
            if ok:
                fd, fstr = factor_degrees(aP)
                entry.update({"L_prym": [int(c) for c in aP], "L_prym_str": fstr, "factor_degrees": fd})
                print("   ", kind, ": genus", gi, "| Prym dim", d, "| L(P) factor degrees", fd, "| %.0fs" % (time.time() - t1), flush=True)
            else:
                entry["L_prym_rational"] = [str(c) for c in aP]
                print("   ", kind, ": genus", gi, "| Prym dim", d, "| WEIL CHECK FAILED:", why, "| %.0fs" % (time.time() - t1), flush=True)
            if validate and ok:
                t2 = time.time()
                Lfull_int = list(Li.L_polynomial())
                Tt = PolynomialRing(ZZ, 't')
                prod = Tt([ZZ(c) for c in afull]) * Tt([ZZ(c) for c in aP])
                entry["validation"] = {"L_full_quotient_times_L_prym_equals_L_curve": list(prod) == [int(c) for c in Lfull_int], "seconds": float("%.1f" % (time.time() - t2))}
                print("      validation (full L-polynomial of the quotient, places up to degree %d): equal =" % gi, entry["validation"]["L_full_quotient_times_L_prym_equals_L_curve"], "| %.0fs" % (time.time() - t2), flush=True)
            res["curves"][kind] = entry
        res["seconds"] = float("%.1f" % (time.time() - t0))
        out["primes"][str(p)] = res
        json.dump(out, open(outfile, "w"), indent=1)
    print("DONE", fam, flush=True)
