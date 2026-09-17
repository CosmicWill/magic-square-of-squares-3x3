# Universal root functions and an exact reciprocity evaluator

Status, 2026-09-17: an evaluator with exact local controls. It furnishes
necessary local compatibility data for the square roots of a hypothetical
magic square of squares. It excludes nothing. The module was left
untracked by the previous session (`compute/root_reciprocity.py`,
"entry 149"); this note records what it proves and what it cannot do,
and the check `rr.` replays every claim below.

Labels RR.1--RR.4 are local to this note. No campaign ledger, theorem
number or headline predicate changes.

## Notation and exact scope

A Lucas grid is `entries(c, u, v)`, in reading order

    c+u,  c-u-v,  c+v
    c-u+v,  c,    c+u-v
    c-v,  c+u+v,  c-u

with the eight line sums 3c. A magic square of squares (MSS3) is such a
grid with nine distinct nonzero rational squares. Its nine square roots
r_0..r_8 are rational; r_4 is the center root. Throughout, (a,b)_p is the
quadratic Hilbert symbol of Q_p with values in {+1,-1}, and (a,b)_infinity
its real counterpart. The module works in exact rational arithmetic; no
floating point is used anywhere.

## RR.1. The cross entries and the circle

**PROVEN, elementary.** The grids whose five cross entries c, c+-u, c+-v
are rational squares are, up to multiplication by a rational square,
exactly

    entries(1, x^2 - 1, X^2 - 1),      x^2 + y^2 = 2,   X^2 + Y^2 = 2,

with (x,y), (X,Y) rational points of the circle x^2+y^2=2, parametrized by
`circle_pair(t) = ((1+2t-t^2)/(1+t^2), (1-2t-t^2)/(1+t^2))` for rational t,
the point (-1,-1) at t=None. Proof: c is a square, so dividing by c keeps
all five cross entries square and normalizes the center to 1; then
1+u = x^2 and 1-u = y^2 give x^2+y^2 = 2, and conversely every circle point
gives 1+-u squares. The parametrization is the line through (-1,-1) of
slope t; the map covers every rational point once. The four corner
entries 1 +- u +- v = x^2 + X^2 - 1 and the like are the unsolved
conditions.

Control: t = 1/5, 1/15 give u = 120/169, v = 3360/12769 and the grid with
roots 17/13, 127/113, 1, 97/113, 7/13 at the cross and four corners that
are positive, distinct, and not rational squares: the classical
five-square configuration, replayed by `candidate_report`.

## RR.2. Reciprocity of the root ratios says nothing by itself

**PROVEN, trivial.** For a rational MSS3 the two ratios a = r_0/r_4,
b = r_2/r_4 (the top corners over the center) are nonzero rationals, so
Hilbert reciprocity gives

    prod_v (a, b)_v = 1

over all places v. `symbol_profile(a, b)` lists the finitely many places
with symbol -1; their number is even for every rational pair, as the
control (113/114, 17/114) shows: -1 exactly at 3 and 113. Consequently no
rational pair can be rejected by this identity. The only possible use is
indirect: if the magic equations forced the local symbols at every place
of a hypothetical solution, and forced an odd number of -1, reciprocity
would contradict. RR.4 shows the local values are not forced.

## RR.3. The local symbol from residues

**PROVEN.** For an odd prime p and integer residues r_0..r_8 modulo p^k
satisfying the eight magic equations modulo p^k, with nine distinct
nonzero squares and with the unit parts of the slots r_0, r_2, r_4 known
modulo p (modulo 8 when p = 2), the symbol (r_0/r_4, r_2/r_4)_p is
determined by those residues. `local_root_symbol` evaluates it after
checking each of these conditions and refuses otherwise. The formulas
are the standard ones (Serre, *A Course in Arithmetic*, III.1.2): for odd
p and units u, w, (p^i u, p^j w)_p = (-1)^{ij(p-1)/2} (u/p)^j (w/p)^i;
at 2 the formula with the characters mod 8. The check verifies the
implementation against symmetry, bilinearity, (a,-a) = (a,1-a) = 1, the
product formula on a grid of rational pairs, and the tabulated values.

Residues certify only the finite congruences; they never certify the
existence of a p-adic or rational lift.

## RR.4. The local symbol is not forced by the local equations

**PROVEN by exact controls.**

1. A full Q_113 point with symbol -1. The grid (c,u,v) =
   (114^2, -227, -12707) has three exact integer roots 113, 17, 114 at
   the slots r_0, r_2, r_4 and six further entries that are simple unit
   squares modulo 113, so all nine roots exist in Q_113 by Hensel's lemma
   (`nontrivial_control`, precision 113^8). Its nine entries are positive
   and distinct integers. The symbol (113/114, 17/114)_113 = -1.
2. Full Q_p points with symbol +1 at p = 2, 3, 113. `fourth_power_control`
   builds `entries(1, t, 3t)` with t = 16 (p = 2) or t = p^2 and lifts
   fourth roots of every entry, so every root slot is itself a p-adic
   square and the symbol is +1. These are local configurations only:
   several entries are negative integers, so they are not real points.

So at 113 both values of the symbol occur among full local points, and at
2 and 3 the value +1 occurs. Nothing forces the symbol at any tested
place, and no odd count of -1 can be derived locally. Whether -1 also
occurs among full Q_2 or Q_3 points is not determined here.

**FAILED-ATTEMPT as an exclusion.** Reciprocity of (r_0/r_4, r_2/r_4)
cannot by itself constrain rational MSS3: the local profile is free at
the places examined, and reciprocity is an identity for rational data.
Any use would need a global restriction of the local profiles that the
rational points of the surface (or of a cover with the retained
conditions) actually realize; no such restriction is known, and the GB.3
barrier applies to finite Brauer-type restrictions on the open surface.

## Reproduction and provenance

```text
python -m compute.root_reciprocity
python -m compute.root_reciprocity --candidate -41496/180625 138600/180625
python -m compute.root_reciprocity --circle 1/5 1/15
python -m compute.root_reciprocity --symbol 113/114 17/114
python -m verify --only rr.
```

The module is exact (fractions, Hensel lifting with simple roots, no
floating point). The classical Hilbert-symbol formulas are CITED; the
circle parametrization is proved above. The controls are finite exact
certificates for the stated local configurations. No source outside the
repository was consulted for this note.
