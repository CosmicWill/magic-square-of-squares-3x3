"""M12-B (ROADMAP W4): the mechanism of the 36 beyond-genus kills —
characters, product sets, and the H-Redei test.

THE QUESTION (A9-T1 fourth layer, verbatim): what invariant of
(2m^2, 2m^2 +- X) separates the three representing sets inside one
genus?  ROADMAP W4's hypothesis H-Redei proposes exact reciprocity
(Redei-symbol level) laws.  This probe computes, for every GLOBAL kill
behind the m <= 1200 pair desert, on every admitting stratum:

  1. the class group Cl(D) as an abstract abelian group (generator/
     relation construction from Gauss composition; the full character
     table, exact, as Q/Z-valued pairings);
  2. the representing sets S_j = {classes representing th_j} (brute
     ground truth, inverse-closed by (a,b,c) ~ (a,-b,c));
  3. the IDEAL-PRODUCT MODEL: for th_j coprime to the conductor,
     S_j should equal  c_3^{v_3} * prod_{p split, p^e || th_j}
     {P_p^k : |k| <= e, k == e mod 2}  (inert primes contribute
     nothing after their forced even valuations) — the classical
     norm-factorization law, machine-checked here on kill data;
  4. SEPARATION ANALYSIS: which kills admit a CHARACTER certificate
     (a character of Cl constant on two of the three sets with
     different constants — by inverse-closure such constants are
     forced to be +-1, so odd-order class groups can never be
     separated by characters), and which are separated only by the
     product-set geometry itself (empty triple intersection with no
     character reason — the "arc" mechanism).

The verdict distribution CHARACTER vs ARC vs conductor-entangled is
the empirical answer to whether the fourth sieve is Redei-type
reciprocity or something genuinely new.  Run:

    python -m compute.redei_probe [--full]

(default: the two m = 725 pairs, the sharpest instance; --full runs
all 11 passers / 36 GLOBAL lines).
"""

import sys
from fractions import Fraction
from math import gcd

from compute.sphere_composition import (PASSERS_1200, compose, genera,
                                        killed_lines, line_anatomy,
                                        principal_form, prims, strata)
from compute.sphere_gluing import legendre, represents


# --------------------------------------------------------------- structure

def abelian_structure(D):
    """Generator/relation presentation of Cl(D) from composition:
    returns (gens, rels, dlog) with dlog: form -> {gen_index: exp}
    and rels[i] = (k_i, word_i) meaning g_i^{k_i} = word_i (a dlog
    dict over earlier generators)."""
    forms = prims(D)
    e0 = principal_form(D)
    dlog = {e0: {}}
    gens, rels = [], []
    for f in forms:
        if f in dlog:
            continue
        chain = []
        x = f
        while x not in dlog:
            chain.append(x)
            x = compose(x, f, D)
        k = len(chain) + 1          # f^k = x in span
        gi = len(gens)
        gens.append(f)
        rels.append((k, dict(dlog[x])))
        items = list(dlog.items())
        for s, vec in items:
            y = s
            for j in range(1, k):
                y = compose(y, f, D)
                nv = dict(vec)
                nv[gi] = j
                dlog[y] = nv
    assert len(dlog) == len(forms)
    return gens, rels, dlog


def characters(D):
    """All |Cl(D)| characters, exactly: each is a dict form ->
    Fraction mod 1 (additive), built recursively from the triangular
    relations."""
    gens, rels, dlog = abelian_structure(D)
    assigns = [dict()]
    for i, (k, word) in enumerate(rels):
        new = []
        for a in assigns:
            wval = sum((a[j] * e for j, e in word.items()),
                       Fraction(0)) % 1
            for t in range(k):
                b = dict(a)
                b[i] = (Fraction(t, k) + wval / k) % 1
                # consistency: k * b[i] == wval (mod 1)  by construction
                new.append(b)
        assigns = new
    out = []
    for a in assigns:
        table = {}
        for f, vec in dlog.items():
            table[f] = sum((a[i] * e for i, e in vec.items()),
                           Fraction(0)) % 1
        out.append(table)
    return out, dlog


def char_order(table):
    from math import lcm
    o = 1
    for v in table.values():
        o = lcm(o, v.denominator)
    return o


# --------------------------------------------------------------- the model

def factorize(n):
    out = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def class_of_prime(D, p):
    """A form representing the prime p (one of the two conjugate
    prime classes for split p; the ramified class for p | D with p
    coprime to the conductor); None if no class represents p."""
    for f in prims(D):
        if represents(f, p):
            return f
    return None


def model_set(D, w):
    """The ideal-product prediction for the representing classes of w
    (None if w is entangled with the conductor, i.e. shares a prime
    with it — the non-invertible-ideal regime)."""
    cond2 = (-D) // 3          # conductor^2 (D = -3 k^2)
    fac = factorize(w)
    cur = {principal_form(D)}
    for p, e in fac.items():
        if cond2 % p == 0:
            return None                        # conductor-entangled
        sym = legendre(D % p, p) if p != 2 else None
        if p == 2:
            return None                        # w is odd in our data
        if D % p == 0:                          # ramified (p = 3)
            c3 = class_of_prime(D, p)
            if c3 is None:
                return set()
            step = c3
            for _ in range(e):
                cur = {compose(x, step, D) for x in cur}
        elif sym == -1:                         # inert
            if e % 2:
                return set()
        else:                                   # split
            P = class_of_prime(D, p)
            if P is None:
                return set()
            powers = {}
            x = principal_form(D)
            for k in range(e + 1):
                powers[k] = x
                x = compose(x, P, D)
            Pinv = (P[0], -P[1], P[2])
            from compute.sphere_classes import reduce_form
            Pinv = reduce_form(*Pinv)
            xs = {}
            x = principal_form(D)
            for k in range(e + 1):
                xs[-k] = x
                x = compose(x, Pinv, D)
            ks = [k for k in range(-e, e + 1) if (e - k) % 2 == 0]
            fs = []
            for k in ks:
                fs.append(powers[k] if k >= 0 else xs[k])
            cur = {compose(a, b, D) for a in cur for b in fs}
    return cur


# --------------------------------------------------------------- analysis

def analyze_line(tri, n, verbose=True):
    """Full mechanism analysis of one killed line; returns a verdict
    dict for the first admitting stratum (GLOBAL lines only)."""
    verdict, info = line_anatomy(tri, n)
    if verdict != "GLOBAL":
        return {"verdict": verdict}
    for g, ct, D, th in strata(tri, n):
        pf = prims(D)
        if not pf:
            continue
        S = [frozenset(f for f in pf if represents(f, t)) for t in th]
        if not all(S):
            continue
        gen_map = genera(D)
        admitting = [key for key, gv in gen_map.items()
                     if all(gv & S[i] for i in range(3))]
        if not admitting:
            continue
        # ground truth: the kill
        inter = S[0] & S[1] & S[2]
        assert not inter, "not actually killed?"
        pairwise = [len(S[0] & S[1]), len(S[0] & S[2]),
                    len(S[1] & S[2])]
        # model check
        model = [model_set(D, t) for t in th]
        model_status = []
        for j in range(3):
            if model[j] is None:
                model_status.append("entangled")
            else:
                model_status.append("EXACT" if model[j] == set(S[j])
                                   else "MISMATCH")
        # character separation
        chars, dlog = characters(D)
        h = len(chars)
        seps = []
        for table in chars:
            o = char_order(table)
            if o == 1:
                continue
            vals = []
            const = True
            for j in range(3):
                vj = {table[f] for f in S[j]}
                if len(vj) == 1:
                    vals.append(vj.pop())
                else:
                    vals.append(None)
            pairs = [(i, j) for i in range(3) for j in range(i + 1, 3)
                     if vals[i] is not None and vals[j] is not None
                     and vals[i] != vals[j]]
            if pairs:
                seps.append((o, pairs, vals))
        mech = "CHARACTER" if seps else "ARC"
        row = {"verdict": "GLOBAL", "stratum": (g, ct, D),
               "h": h, "genus_sizes": sorted(len(v) for v in
                                             gen_map.values()),
               "S_sizes": [len(s) for s in S],
               "pairwise": pairwise, "mechanism": mech,
               "separators": [(o, p) for o, p, _ in seps[:4]],
               "model": model_status, "th": th}
        if verbose:
            print(f"    stratum (g={g}, ct={ct}, D={D}): h = {h}, "
                  f"|S| = {row['S_sizes']}, pairwise "
                  f"{pairwise}, triple 0")
            print(f"      model: {model_status}   mechanism: {mech}"
                  + (f"   separators (order, pairs): "
                     f"{row['separators']}" if seps else ""))
        return row
    return {"verdict": "GLOBAL", "mechanism": "no-admitting-stratum?"}


def analyze(pairs, verbose=True):
    stats = {"CHARACTER": 0, "ARC": 0, "L0": 0, "GENUS": 0}
    model_stats = {"EXACT": 0, "MISMATCH": 0, "entangled": 0}
    rows = []
    for m, U, V in pairs:
        n = 3 * m * m
        if verbose:
            print(f"pair m={m} (U,V)=({U},{V}):")
        for i, tri in killed_lines(m, U, V):
            if verbose:
                print(f"  line {i}: tri = {tri}")
            row = analyze_line(tri, n, verbose=verbose)
            row["pair"] = (m, U, V)
            row["line"] = i
            rows.append(row)
            v = row.get("mechanism", row["verdict"])
            if v in stats:
                stats[v] += 1
            elif row["verdict"] in stats:
                stats[row["verdict"]] += 1
            for s in row.get("model", []):
                model_stats[s] += 1
    return rows, stats, model_stats


def main():
    full = "--full" in sys.argv
    pairs = PASSERS_1200 if full else [p for p in PASSERS_1200
                                       if p[0] == 725]
    rows, stats, model_stats = analyze(pairs)
    print()
    print(f"== M12-B verdicts over {'all 11 passers' if full else 'm = 725'} ==")
    print(f"kill mechanisms: {stats}")
    print(f"ideal-product model on GLOBAL values: {model_stats}")
    arc = [r for r in rows if r.get("mechanism") == "ARC"]
    if arc:
        print("ARC kills (no character certificate exists — the "
              "fourth-sieve law is NOT pure reciprocity there):")
        for r in arc:
            print(f"  m={r['pair'][0]} line {r['line']} "
                  f"stratum {r['stratum']} h={r['h']} "
                  f"genus sizes {r['genus_sizes']}")


if __name__ == "__main__":
    main()
