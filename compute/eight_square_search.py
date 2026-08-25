"""Eight-square taxonomy sweep (docs/attacks/A4-eight-squares.md).

For every center value c (square or not) up to a bound, compute
Dtilde(c) = {d > 0 : c-d and c+d are both perfect squares} and test the
additive patterns that the 8- and 9-square configurations force:

  QUADRUPLE  u, v, u+v, u-v in Dtilde(c)
      -> MSS3 if c is a square; class-C 8-square (non-square center) else.
  TRIPLE     d1, d2, d1+d2 in Dtilde(c)
      -> three-full-AP >= 7-square configuration (class E needs c square
         plus a one-sided extra) — extends the A3.3 additive desert from
         square centers to ALL centers.
  K-PATTERN  d, e, 2d+e in Dtilde(c), c square, c+d+e square
      -> class-K (corner) 8-square candidate.

It also runs a direct census: for every pair d_a != d_b in Dtilde(c) and
each of the four slot-assignments, count the perfect squares among the
nine entries of L(c, u, v); any configuration with >= 7 squares and nine
distinct entries is reported.  The Bremner–Sallows square AB1 MUST be
re-found at c = 425^2 (validation of the machinery).

Run:  python3 -m compute.eight_square_search [BOUND]
"""

import sys
from math import isqrt


def is_square(n):
    return n >= 0 and isqrt(n) ** 2 == n


def dtilde(c):
    out = []
    q = isqrt(c) + 1
    while q * q <= 2 * c:
        d = q * q - c
        if is_square(c - d):
            out.append(d)
        q += 1
    return out


LUCAS = ((1, 1, 0), (1, -1, -1), (1, 0, 1),
         (1, -1, 1), (1, 0, 0), (1, 1, -1),
         (1, 0, -1), (1, 1, 1), (1, -1, 0))


def census_entries(c, u, v):
    return [a * c + b * u + e * v for (a, b, e) in LUCAS]


def sweep(bound, census=True):
    quads, triples, kpat, sevens = [], [], [], []
    for c in range(1, bound + 1):
        D = dtilde(c)
        if len(D) < 2:
            continue
        Ds = set(D)
        c_square = is_square(c)
        for i, d1 in enumerate(D):
            for d2 in D[:i]:
                if d1 + d2 in Ds:
                    triples.append((c, d1, d2))
                    if d1 - d2 in Ds:
                        quads.append((c, d1, d2))
                if c_square and 2 * d2 + d1 in Ds and is_square(c + d1 + d2):
                    kpat.append((c, d2, d1))
        if census:
            for d_a in D:
                for d_b in D:
                    if d_a == d_b:
                        continue
                    forms = [(d_b, d_a), (d_b - d_a, d_a), (d_a + d_b, d_a)]
                    if (d_a + d_b) % 2 == 0:
                        forms.append(((d_a + d_b) // 2, (d_a - d_b) // 2))
                    for (u, v) in forms:
                        ents = census_entries(c, u, v)
                        if len(set(ents)) != 9 or min(ents) < 0:
                            continue
                        nsq = sum(is_square(e) for e in ents)
                        if nsq >= 7:
                            sevens.append((c, u, v, nsq))
    return quads, triples, kpat, sevens


def main():
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    quads, triples, kpat, sevens = sweep(bound)
    print(f"bound={bound}")
    print(f"  additive QUADRUPLES (MSS3 / class-C): {len(quads)} {quads[:3]}")
    print(f"  additive TRIPLES (any center):        {len(triples)} {triples[:3]}")
    print(f"  K-PATTERNS with half-condition:       {len(kpat)} {kpat[:3]}")
    uniq = {}
    for c, u, v, nsq in sevens:
        uniq.setdefault((c, frozenset((abs(u), abs(v)))), (c, u, v, nsq))
    print(f"  >=7-square configurations (deduped):  {len(uniq)}")
    for k, (c, u, v, nsq) in sorted(uniq.items())[:10]:
        print(f"      c={c} (root {isqrt(c) if is_square(c) else '-'}), "
              f"u={u}, v={v}: {nsq} squares")


if __name__ == "__main__":
    main()
