# Global-obstruction investigation: the first boundary audit

2026-09-09. Branch `research/proof-alternatives`, based on
`a719b635e7ca969ef62a805d85c0a9d6b5fbc17e` (main through entry 140).

This checkpoint finds limitations on a proof method, not new exclusions of
magic squares. In particular, **a finite list of ordinary Brauer classes on
the full admissible open surface cannot make its adelic set empty** (GB.3,
**CITED** consequence of Harari's formal lemma). This is stronger than the
existing warning that degenerate rational points prevent an obstruction on
the complete surface: deleting the degeneracies does not fix the finite-list
strategy, even if the classes ramify on the deleted locus.

The next candidate is a cover defined by three sums of entry roots (GB.7).
It retains component/sign information that the entry-line symbols discard.
An explicit twist is locally soluble everywhere, avoids all signed all-equal
rational fibers, and has no rational lift on one AP axis. Its other AP axis
remains unresolved. No cover has yet been certified to give
an obstruction, and no authoritative campaign verdict is changed.

## Model and scope

Work in characteristic zero. Normalize the center root to 1 and put

\[
 l_{a,b}=1+au+bv,\qquad
 r_{a,b}^2=l_{a,b},\qquad
 (a,b)\in\{-1,0,1\}^2\setminus\{(0,0)\}.
\]

Let V be the affine surface where the eight r's are invertible. Let U be
its open subset where

\[
 D=uv(u-v)(u+v)(u-2v)(u+2v)(2u-v)(2u+v)\ne0.
\]

These are the nine entry lines, including the projective center line,
and eight further distinctness lines. The older W2/W3 roadmap's references
to twelve branch lines do not describe this cover; A5 section 2 and the
A8 character atlas use nine. This note does not edit historical documents.

U(Q) is the original admissible problem, after normalization and clearing
denominators. The center cannot be zero for a nontrivial rational square
configuration: an opposite pair would sum to zero and both real squares
would vanish. F4.1, after primitive integral scaling, excludes a zero entry.
F1.3 gives precisely the eight factors of D. There is no added positivity
assumption over Q: rational squares are nonnegative, and here nonzero.

V contains P0=(u,v,r)=(0,0,1,...,1). This is a smooth rational point,
although it is excluded from U. The Jacobian of the eight equations has
the invertible diagonal root block diag(2r). Distinct affine linear
radicands have independent square classes over Qbar(u,v), by their
separate order-one valuations. Thus V is smooth and geometrically integral,
and its degree over the entry-line complement is 256.

## GB.1 — Entry-monomial symbols collapse

**PROVEN.** For K=Q(u,v) and F=K(r_{a,b}), let

\[
 f=A\prod l_i^{e_i},\qquad g=B\prod l_i^{f_i},
 \quad A,B\in\mathbb Q^*,\quad e_i,f_i\in\mathbb Z.
\]

The quaternion algebra (f,g) over F is isomorphic to (A,B). In particular,
if either slot has constant factor 1, the algebra is split. Finite sums of
these symbols pull back to constants. Constants are not necessarily split;
their evaluations have zero total invariant by global reciprocity.

Proof: f=A R^2 and g=B S^2 with R,S the corresponding root monomials.
Rescale the two quaternion generators by R and S. When the first slot is
squared, an explicit matrix realization is

\[
 I=\begin{pmatrix}R&0\\0&-R\end{pmatrix},\qquad
 J=\begin{pmatrix}0&g\\1&0\end{pmatrix}.
\]

These satisfy I^2=R^2, J^2=g, IJ=-JI; 1,I,J,IJ are independent for Rg!=0.
They identify the algebra with M_2(F). This proof includes negative powers
and retains every rational constant and sign.

This only classifies the displayed symbol family. It does not compute
Br(V), Br(U), or all classes descending from intermediate quotients.
Ford's Theorem 1.1 supplies relevant arrangement-symbol background over an
**algebraically closed** field; it is not a theorem identifying Br(U) over Q.

## GB.2 — The original cover has no useful twist label on full squares

**PROVEN.** On the entry-line complement the original cover is
r_i^2=l_i. Its square-class fiber invariant is ([l_i]) in
(k*/k*2)^8. A rational point already satisfying all nine square conditions
has invariant (1,...,1). This includes P0, nonconstant degenerate AP
configurations, and every hypothetical admissible point.

Equivalently, in the convention d_i z_i^2=l_i, such a point lifts only to
the trivial twist class [d_i]=1. Therefore this particular twist invariant
cannot separate admissible points from degenerate ones. A new descent on
V or U needs a different covering map; it cannot reuse these eight square
roots and assume that admissible points occupy different twists.

The elementary check uses P0 and (u,v)=(0,120/169), whose values are
1,49/169,289/169 with repetitions. AB1 has only seven square entries and
is deliberately not treated as a rational point of V.

## GB.3 — Finite ordinary Brauer tests cannot exclude U(Q)

**CITED.** For every finite subgroup B of Br(U),

\[
                         U(\mathbb A_{\mathbb Q})^B\ne\varnothing.
\]

The same holds for any finite collection of classes: a finite collection
of torsion elements generates a finite subgroup. The real component can
be chosen with all entry roots positive and nine distinct entries.

Here the adeles are those of the open variety U: points must be integral
in a model of U at almost all primes. Merely giving local points that
reduce to the deleted degeneracy at every prime would not prove this.

Derivation, with the imported ingredients explicit:

1. Put B0=B intersect Br(V), using the injective restriction into Br(U).
   Choose a finite set S containing infinity, bad model primes, primes
   needed to extend these finitely many classes, and the support of their
   evaluations at P0. Outside S, integral evaluations are zero. Enlarge
   S so U has smooth integral points at all remaining primes: spread out
   its geometric integrality and apply Lang--Weil, then Hensel.
2. At each place of S choose a point of U close enough to P0 that every
   B0-evaluation equals its value at P0. Local constancy gives the
   evaluation equality. Existence arbitrarily close is explicit: take
   u=t, v=3t and the roots near 1, with t nonzero and sufficiently small.
   At the real place take small positive t. Outside S choose any of the
   integral points just obtained. Reciprocity for the rational classes
   evaluated at P0 makes this adelic point orthogonal to B0.
3. Apply Harari's formal lemma to U inside V and B. It changes components
   outside S to obtain orthogonality to all of B, preserving the chosen
   components at S. This gives the asserted adelic point and preserves
   the positive real configuration.

The lemma is stated in the Colliot-Thelene--Skorobogatov author manuscript
as Theorem 12.6.3 (printed p.264; PDF page 264), with B intersect Br(V)
as its hypothesis. It is Harari's 1994 Corollary 2.6.1. Local constancy is
Proposition 9.5.2 in that manuscript. These external theorems are not
reproved by the Python suite, so this conclusion is tagged CITED rather
than PROVEN under this repository's protocol.

**Limits.** This does not assert nonemptiness for the entire possibly
infinite Br(U), and it says nothing about U(Q). The adelic witness may
depend on B; one cannot interchange these quantifiers. The statement
does not exclude a descent through other covers, point arithmetic on
fibers, or an integral obstruction after a justified restriction of
denominators. Any attempt to fix an integral model at every prime must
explain why it covers every primitive integer candidate.

The practical consequence is that a successful finite Brauer computation
on this U can constrain points but cannot finish by U(A)^B being empty.
Deleting more divisors from V also leaves this argument available for any
nonempty open subset. A proposed auxiliary cover should first be checked
for a smooth rational boundary point or such a point on a smooth model.

## GB.4 — A nontrivial symbol and stronger local controls

**PROVEN.** The root-dependent quaternion

\[
                \alpha=(r_{1,0},r_{0,1})
\]

is geometrically nontrivial in the function-field Brauer group. Both slots
are units on V, so it defines an Azumaya algebra there. It ramifies on a
divisor over the entry line 1+u=0 on a larger smooth model.

Proof of nontriviality: over Qbar take the point above u=v=-1 where
s=r_{1,0}=0 and t=r_{0,1}=0. Only those two entry roots vanish. Substitute
u=s^2-1, v=t^2-1. The other six radicands have nonzero constant terms,
so their roots give an etale local chart in s,t. On the divisor s=0,
t has a simple zero and is not a square in its function field. If (s,t)
split, t would be a norm from adjoining sqrt(s). In the completion at
s=0 a unit norm a^2-s b^2 has square residue: the two terms have valuations
of different parity, so a unit norm forces a to be a unit and b integral.
The nonsquare residue t contradicts this. It also gives the nonzero tame
residue, showing ramification. At P0 both slots are 1, so this class is
regular there and its value is zero; GB.3 applies.

**PROVEN.** There are local admissible configurations near P0 for which
all nine entries are fourth powers, hence all chosen entry roots themselves
are squares. For odd p take u=p^2, v=3p^2; at p=2 take u=16, v=48.
Every entry is 1 modulo p, respectively 16. For odd p, lifting a fourth
root near 1 uses the invertible derivative 4x^3. For 2, start with x=1,
which solves the fourth-power equation modulo 16. At stage n>=4,
replacing x by x+2^(n-2) changes x^4 by
2^n modulo 2^(n+1). Choose one of these two values at each step.
The limits give fourth roots. Distinctness holds in Q_p since the offsets
are t times the nine different integers -4,...,4.

**VERIFIED(p<=499, precision p^8 for odd p and 2^20).** The script supplies
and checks all nine fourth roots at 95 primes. This is a local control,
not by itself an adelic or rational solution. Over R use u=1/100,v=3/100.

## GB.5 — Homogeneous direction covers have a boundary trap

Let L_j be distinct members of the eight homogeneous factors of D. Define
an auxiliary cover of V by

\[
                       d_j z_j^2=L_j(u,v),\qquad d_j\in\mathbb Q^*.
\]

**PROVEN.** For one or two L_j, every twist has a smooth rational point
above P0, with every z_j=0. Its Jacobian has rank 8+k for k<=2: the eight
root columns give rank 8 and the k distinct homogeneous line forms give
rank k in u,v. Each cover is geometrically integral: the new line
radicands have independent valuation coordinates alongside the eight
entry radicands. GB.3 therefore applies to its admissible open subset.
All 8 single-line and 28 two-line choices are checked, independently of d.

For k>=3, choose L_1,L_2 as a basis and write L_j=A_j L_1+B_j L_2. There
is a projective direction curve

\[
 C_d:\quad d_j Z_j^2=A_jd_1Z_1^2+B_jd_2Z_2^2\quad(j=3,...,k).
\]

**PROVEN.** Every admissible rational point of the cover maps to C_d(Q).
Conversely, a rational point of this smooth direction curve supplies a
smooth rational boundary point on a model of the cover above P0. In a
chart Z_i!=0 put z_j=w Z_j/Z_i, solve u,v from the first two equations,
and keep the entry roots. At w=0 they are all 1. The local model is
etale over the product of the smooth direction curve and the w-line.
This constructs the boundary point without assuming a rational point
in the admissible open.

The direction curve is smooth: distinct L's imply at most one Z_j can
vanish at a projective point. A Jacobian dependence would give a linear
relation among the L's supported on that single index, which is impossible.
Over Qbar it is the connected degree 2^(k-1) cover of P^1 obtained by
adjoining sqrt(L_j/L_1), with simple order-two inertia at the k directions.

**CITED.** For k=3 the direction curve is a smooth conic. If the cover is
everywhere locally soluble, the conic is too; Hasse--Minkowski supplies a
rational point. Consequently finite ordinary Brauer tests cannot rule
out an everywhere locally soluble three-line twist either. The suite
checks all 56 exact conic equations, not Hasse--Minkowski itself.

For any k the distinction matters: if C_d(Q) is empty, the twist has no
admissible rational point already by projection. If C_d(Q) is nonempty,
its smooth rational boundary point triggers GB.3 on the covering surface.
Thus merely adding more homogeneous direction roots does not provide a
finite-Brauer endgame for the twists whose directions are rationally
realizable. A genuine new step is required.

## GB.6 — Four-line boundary atlas, retained as reference data

**CITED.** For k=4 the direction curve has genus one: Riemann--Hurwitz
gives 2g-2=8(-2)+4(8/2)=0. Its branch double cover has equation
y^2=product L_j on P^1. The degree-four map to that double cover is
unramified: its three nontrivial deck transformations flip two coordinates,
which has no fixed point because two coordinates cannot vanish together.
Over Qbar these are the three translations by nonzero 2-torsion points
of the genus-one curve, so quotienting has the same geometric j-invariant.
This does not identify the Q-torsor or its rational points.

**VERIFIED(exhaustive 70 subsets, all 24 orderings).** The eight directions
are {infinity,0,1,-1,1/2,-1/2,2,-2}. Their four-element subsets have 11
geometric cross-ratio types. For the indicated representative lambda,
j=256(1-lambda+lambda^2)^3/(lambda^2(1-lambda)^2).

| lambda | Subsets | j |
|---|---:|---|
| -9 | 2 | 48228544/2025 |
| -8 | 2 | 1556068/81 |
| -5 | 4 | 1906624/225 |
| -4 | 6 | 148176/25 |
| -3 | 10 | 35152/9 |
| -2 | 16 | 21952/9 |
| -16/9 | 1 | 111284641/50625 |
| -5/3 | 4 | 470596/225 |
| -3/2 | 8 | 438976/225 |
| -5/4 | 4 | 3631696/2025 |
| -1 | 13 | 1728 |

This atlas was generated while testing the homogeneous-cover idea. GB.5
explains why it is not automatically a queue of promising obstruction
computations. Preserve it as an exact description of that limitation.

## GB.7 — Next candidate: a triangle of sums of entry roots

Take A=r_(1,0), B=r_(0,1), C=r_(-1,-1). These are a row of the square,
so A^2+B^2+C^2=3. On U, A+B, B+C, C+A are nonzero: a vanishing sum
would make the corresponding entries equal. Consider the etale cover

\[
 d_1 z_1^2=A+B,\qquad d_2 z_2^2=B+C,\qquad d_3 z_3^2=C+A.
\]

Every rational point of U lifts to a twist, taking d_i to represent the
three rational square classes of these sums. This is a different map
from GB.2. The sums distinguish components of equal-entry divisors because
(A+B)(A-B)=u-v; they are not entry monomials.

**PROVEN (all-equal fiber only).** A twist has a rational point above
some signed all-equal configuration iff at least one d_i has square class
2 or -2. At such a configuration (A,B,C) belongs to {+1,-1}^3. An odd
cycle cannot have all three pair sums zero. A nonzero pair sum is +2 or
-2, proving necessity. Conversely, assign equal signs to the chosen edge
and the opposite sign to the third vertex. Exactly that edge sum is
nonzero; the other two z's can be zero. This proves sufficiency.

The root-sign choices here are essential: inspecting only A=B=C=1
would give an incorrect, much stronger exclusion of boundary fibers.
In particular, (d_1,d_2,d_3)=(3,5,7) avoids every signed all-equal fiber;
(2,3,5) does not. Tests cover 216 twist triples and all eight sign patterns.
The remaining five noncentral root signs do not occur in these equations,
so the eight patterns cover all 256 signed points on V above u=v=0.

The (3,5,7) control is unsuitable for a locally soluble candidate: all three
twists are odd. At 2 all normalized entry roots of a local square grid are
odd units (apply the primitive mod-4 argument of F4 to 2-adic roots after
clearing their denominators). Each pair sum would then be an even square
times an odd unit, hence divisible by 4. Around an odd cycle, A+B=B+C=C+A=0
modulo 4 would force the odd root A to be even. This is an elementary local
obstruction to that cover, not a new obstruction to MSS3.

### A locally soluble test case

Set q=(17,89,1513), with q_3=q_1q_2, and choose

\[
                         d=(34,178,3026)=2q.
\]

**PROVEN.** This twist has no rational point above any signed all-equal
configuration, but has a smooth such point over every completion of Q.
Consequently its admissible open has local points at every place.

No q_i is a rational square, so the rational-fiber criterion just proved
excludes all signed all-equal fibers. For each place, however, at least
one q_i is a local square:

- At an odd prime outside {17,89}, the quadratic characters of the three
  units are (epsilon_1,epsilon_2,epsilon_1 epsilon_2). They cannot all be -1.
- At 17, 89=2^2 modulo 17; at 89, 17=27^2 modulo 89. Hensel lifts the
  respective unit square roots.
- At 2 all three q_i are 1 modulo 8. At the real place they are positive.

For a local square q_i, set the two endpoint roots of that edge to +1
and the third root to -1. Then its pair sum is 2 and z_i^2=1/q_i has a
local solution; the other two z's are zero. Smoothness is important here:
the nonzero z_i supplies a pivot, and the differentials of the two
vanishing root sums are independent in u,v. For the edge A+B these are
(du+2dv)/2 and (2du+dv)/2, with determinant -3/4; the other edges are
permutations. This is nonzero over every Q_p, including Q_3. The other
root equations have invertible root derivatives over the local field.
One can produce the nearby points using only square-root lifting: for the
edge A+B put h=d_2 z_2^2, k=d_3 z_3^2 and

\[
 C={h+k-\sqrt{9-2h^2+2hk-2k^2}\over3},\qquad
 A=k-C,\quad B=h-C.
\]

Take h,k sufficiently small and the radical near 3. The row-square sum
is exactly 3. The remaining nonzero-edge square root and the other entry
roots lift from their nonzero local values. The leading terms of (u,v)
are (2(2k-h)/3,2(2h-k)/3); this invertible linear map lets one avoid the
eight distinctness lines by a generic small choice of the two free z's.
This also works at 3 by making h,k sufficiently divisible before lifting.

The covering surface is geometrically integral of degree 8 over V.
Indeed, each of A+B, B+C, C+A has a simple zero along its own component of
an equal-entry divisor, with the other two sums generically nonzero.
For example (A+B)(A-B)=u-v and A-B!=0 generically on A+B=0. The three
order-one valuations prove square-class independence, also over Qbar.
Every component of the finite cover dominates V, so the admissible open
is dense; the local perturbation above can avoid all eight deleted lines.
With this geometric integrality, Lang--Weil and Hensel also produce integral
points at almost all primes: **CITED**, the local points can be chosen to
form an adelic point of the admissible covering open.

This example is a test of the method, not a required twist for every MSS3.
The full family of arbitrary twists covers U(Q). Restricting to this
particular d, or to q_3=q_1q_2, has not been justified for all candidates.

### The two rational AP axes

Write the conic of row roots as

\[
 B=(1-2t-t^2)/(1+t^2),\qquad C=(1+2t-t^2)/(1+t^2).
\]

On u=0 the constant root A is +1. A=-1 would require B,C>=1 from the
positive twists and their square equations, forcing an already excluded
all-equal configuration. The three squared-cover slots are

\[
 f_1={1-t\over17(1+t^2)},\quad
 f_2={1-t^2\over89(1+t^2)},\quad
 f_3={1+t\over1513(1+t^2)}. \tag{AP-u}
\]

On v=0 the constant root B must similarly be +1, and the slots are

\[
 f_1={1-t\over17(1+t^2)},\quad
 f_2={1+t\over89(1+t^2)},\quad
 f_3={1-t^2\over1513(1+t^2)}. \tag{AP-v}
\]

These are necessary row conditions. They also account for the full base
grid on each AP axis, whose entries are just 1,1+v,1-v, or 1,1+u,1-u,
with repetitions and arbitrary remaining root signs.

**PROVEN.** There is no rational point of the selected cover above v=0.
For the B=+1 case, (AP-v) has no Q_3 point. If t is 3-adically integral,
1+t^2 is a unit. Its reductions t=0,1,-1 make, respectively, f_1, f_2,
f_1 a nonsquare unit modulo 3 (17=89=-1, 1513=1 modulo 3). If t has
negative valuation, f_3 is a unit with residue -1/1513=-1 modulo 3.
The omitted t=infinity has the same nonsquare value for f_3. This covers
every rational parameter, including the branch points. The B=-1 case
was excluded at the real place. This exclusion concerns the boundary
of one twist; it is not an MSS3 exclusion.

The u=0 case is still open. Its useful necessary identity is

\[
 {f_1f_3\over f_2}={1\over17^2(1+t^2)},
\]

so a nonzero lift requires 1+t^2 to be square as well. In the v=0 case
the corresponding identity is f_1f_2/f_3=1/(1+t^2). Each AP covering
curve has degree 8 over the t-line, with five geometric branch points
{-1,1,i,-i,infinity}, and hence genus 3 by Riemann--Hurwitz (**CITED**).
The source code checks finite-field fibers on the normalization by taking
the unit residues of every even-valuation product of radicands. Simply
accepting zero coordinates in the singular affine equations is insufficient.

**VERIFIED(|numerator(t)|<=denominator(t)<=100, reduced t).** A necessary
row-condition search on the two axes found no rational lifts in 12,178
axis/parameter cases. Positive twists force |t|<=1 over R. The omitted
infinite parameter gives a negative pair sum and does not lift over Q.
This bounded check does not settle the u=0 genus-three curve.

**CITED (boundary reduction using the classical four-square AP theorem).**
Of the other six distinctness lines, u=+/-v makes the entries contain five
consecutive terms of an AP of squares; u=+/-2v and 2u=+/-v give seven.
A nonconstant such AP is impossible by F3. The only rational points on
these lines are therefore all-equal ones. F4 also excludes any rational
square grid with a zero entry after primitive integral scaling, whether or
not distinctness holds. Thus any rational boundary point on a proper model
of the selected cover must map to one of the two AP axes or an all-equal
point on the original surface. The latter and the v=0 axis are excluded
above. Over a nonconstant rational point on u=0 the three root sums are
nonzero, so the covering is etale there; no extra exceptional rational
point is hidden by a singular root-sum fiber. This makes (AP-u), with its
projective points handled, the remaining rational-boundary test.

**CONJECTURED (research prospect only).** The root-sum family may contain
twists where global arithmetic usefully constrains admissible lifts.
For the selected twist, the unresolved AP-u boundary is the next precise
test before attempting any finite Brauer obstruction on the surface.

Next work, without launching a campaign yet:

1. Decide the AP-u genus-three boundary curve for (34,178,3026), including
   exceptional fibers and compactification. A smooth rational boundary
   point anywhere would restore GB.3 for that twist.
2. Verify the boundary reduction on the chosen smooth model and determine
   which twist square classes can occur. Retain the all-prime local-solubility
   certificate and geometric-integrality proof, instead of redoing scans.
3. Only for a cover that escapes the preceding tests, construct and
   certify a nontrivial class, its domain/ramification, and evaluations.
   A result must identify a necessary condition for all points in its
   stated scope, rather than merely eliminate an arbitrarily chosen twist.

## Reproduction and evidence boundaries

```text
python -m compute.global_obstruction_probe
python -m compute.global_obstruction_probe --ap-bound 100
python -m verify --only gb.
python -m verify --fast --only a5.
python -m verify --fast --only f5.
python -m verify --only gauntlet
```

The gb checks verify the explicit matrix algebra, radicand bookkeeping,
Jacobian ranks, rational lift controls, 95-prime fourth-root controls,
56 conic identities, 70 four-line subsets, triangle sign fibers, the
all-prime square-character certificate, and the AP boundary reductions.
They do not implement a Brauer-group algorithm, prove the imported
arithmetic theorems, solve any genus-one torsor, or establish an MSS3
impossibility claim. No new obstruction predicate is registered because
this checkpoint asserts no obstruction to any anchor or MSS3.

## Sources and provenance

- Colliot-Thelene and Skorobogatov, *The Brauer--Grothendieck Group*,
  [author manuscript](https://www.imo.universite-paris-saclay.fr/~jean-louis.colliot-thelene/BGgroup_book.pdf).
  **READ, relevant sections only:** 9.5.1 (local constancy), 12.6 (formal
  lemma), and 1.5 (Faddeev background). Numbers refer to this manuscript,
  not the differently numbered published edition. GB.3 is an application
  derived here, not a claim that the book discusses magic squares.
- Harari, *Methode des fibrations et obstruction de Manin*, Duke Math. J.
  75 (1994), 221--260,
  [author PDF](https://www.imo.universite-paris-saclay.fr/~david.harari/articles/duke.pdf).
  **READ, relevant portions:** local density discussion and formal lemma
  2.6.1; original source behind the version used above.
- Ford, *The Brauer Group of an Affine Double Plane Associated to a
  Hyperelliptic Curve*,
  [arXiv:1303.5690](https://arxiv.org/html/1303.5690v1).
  **READ, sections 1--2 in part:** background on arrangement symbols and
  pullback. Not load-bearing for GB.1, and its algebraically closed ground
  field must not be silently replaced by Q.
- Hasse--Minkowski, Lang--Weil, Riemann--Hurwitz and elementary genus-one
  quotient facts are **CITED classical inputs**, not rederived by this
  branch. Their uses are isolated above. The model, normalization and
  existing local controls come from F1, F4, F5 and A5 in this checkout.
  References for the classical formulas include
  [Stacks, Riemann--Hurwitz](https://stacks.math.columbia.edu/tag/0C1B)
  and [Stein, Hasse--Minkowski](https://www.williamstein.org/papers/ant/html/node70.html).
