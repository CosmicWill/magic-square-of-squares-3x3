# Global-obstruction investigation: finite-class barriers and boundary covers

2026-09-09, updated 2026-09-10. Branch `research/proof-alternatives`, based on
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
rational fibers, and now has both AP boundaries excluded. GB.8 settles
the remaining genus-three curve using Tunnell's theorem and proves that
a smooth proper model of this twist has no rational boundary points.
Its admissible rational points remain unknown. No cover has yet been
certified to give an obstruction, and no campaign verdict is changed.

**Current continuation:** [universal-twist-reduction.md](universal-twist-reduction.md).
The owner prioritized the universal reduction. UT.2 gives an explicit
infinite family covering every hypothetical solution; UT.3 constrains its
prime support. UT.4 shows that signs and grid symmetry do not locally force
the product-square subfamily used to select (17,89,1513).

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

The u=0 case was left open at checkpoint 2c91f31. **GB.8 below settles it**
using a genus-one quotient. Its useful necessary identity is

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
This bounded check alone does not settle the u=0 genus-three curve.

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
GB.8 closes the selected twist's rational-boundary test. This does not
establish a finite Brauer obstruction on the covering surface.

## GB.8. The remaining boundary has no rational points (2026-09-10)

**CITED (deduction from Tunnell's unconditional necessary condition).**
The smooth projective AP-u genus-three curve has no rational points.
Consequently the selected cover has no rational point above u=0.
The argument below is complete modulo the stated classical theorem;
its finite arithmetic and rational maps are checked exactly. Neither BSD
nor a conjectural converse to Tunnell's criterion is used.

### The quotient that settles the curve

The second AP-u equation alone gives, on putting y=89(1+t^2)z_2,

\[
                         H:\quad y^2=89(1-t^4).
\]

This is a genus-one quotient of the genus-three curve. For any positive
rational n and a point y^2=n(1-t^4) with ty!=0, the rational numbers

\[
 \left|{y\over t}\right|,\qquad
 \left|{2nt\over y}\right|,\qquad
 \left|{n(1+t^4)\over ty}\right|
\]

are the sides of a nondegenerate right triangle of area n. To check this,
clear denominators in the Pythagorean identity and use
(1-t^4)^2+4t^4=(1+t^4)^2. The product of the two legs is 2n.
Equivalently, the explicit map

\[
             (t,y)\longmapsto (x,Y)=(-nt^2,nty)
\]

lands on Y^2=x^3-n^2x with Y!=0. Thus a nonexceptional rational point
on H would make 89 a congruent number.

### Complete finite certificate for noncongruence of 89

Let N_c(n) count **all signed integer triples** satisfying
2x^2+y^2+c z^2=n. Tunnell's necessary condition for positive odd
squarefree n is N_8(n)=2N_32(n) if n is congruent. In the notation of
his paper, a(n)=N_32(n)-N_8(n)/2, and a(n)!=0 excludes n.
See the theorem on printed p.323 and its ternary-form expression on
p.325 of [Tunnell's original paper](https://sites.math.rutgers.edu/~zeilberg/EM22/JT1983.pdf).

For n=89 the complete nonnegative representatives and their sign weights
are as follows. Each nonzero coordinate contributes a factor of two.

| c | (x,y,z) | Sign weight |
|---|---|---:|
| 8 | (0,9,1) | 4 |
| 8 | (2,3,3) | 8 |
| 8 | (2,7,2) | 8 |
| 8 | (2,9,0) | 4 |
| 8 | (4,5,2) | 8 |
| 8 | (4,7,1) | 8 |
| 8 | (6,3,1) | 8 |
| 32 | (2,7,1) | 8 |
| 32 | (2,9,0) | 4 |
| 32 | (4,5,1) | 8 |

The positive coefficients give the exhaustive bounds |x|<=6, |y|<=9,
|z|<=3 for c=8 and |z|<=1 for c=32. Therefore

\[
             N_8(89)=48\ne40=2N_{32}(89),\qquad a(89)=-4.
\]

This is a complete finite theorem certificate, not a rational-point
height search. `gb.tunnell_89_certificate` compares the nonnegative
enumeration with an independently enumerated signed box. The known
congruent numbers 5 and 15 are positive controls; equality is reported
only as inconclusive.

### Exceptional and projective fibers

The preceding triangle map omits exactly ty=0. On H, t=0 would require
y^2=89 and is impossible over Q. If y=0, then t=+/-1. These give the
two rational points (1,0),(-1,0) on H. Its two geometric points at
infinity have residue equation (y/t^2)^2=-89, so neither is rational.
Thus this argument determines **all** rational points of the smooth
projective H, including infinity.

The function-field inclusion extends to a morphism from the smooth
projective AP-u curve to H. Alternatively the valuation argument is
direct: t is a rational value or infinity at a rational point; at finite
rational t, 1+t^2!=0 and each z_i is integral because its square is
regular. A rational point would therefore specialize every finite slot
to a rational square. At t=1, f_3=1/1513 is nonsquare; at t=-1,
f_1=1/17 is nonsquare. Neither rational point of H lifts. The nonrational
parameters t=+/-i cannot be images of rational points. This deals with
the normalization as well as the raw affine equations.

As an independent diagnostic, PARI/GP 2.17.4 gives the following
Jacobian data for the three single-character elliptic quotients:

| Quotient | Weierstrass coefficients [a1,a2,a3,a4,a6] | ellrank | elltors order |
|---|---|---|---:|
| z_1 | [0,-34,0,578,0] | [1,1,0,[[49/9,1295/27]]] | 2 |
| z_2 | [0,0,0,31684,0] | [0,0,0,[]] | 2 |
| z_3 | [0,-3026,0,4578338,0] | [1,1,0,[[5329,299665]]] | 2 |

The first and third models follow from x=q(1-t), Y=q^2(1+t^2)z_1,
or x=q(1+t), Y=q^2(1+t^2)z_3 respectively, with q=17 or 1513.
The middle Jacobian is returned by `ellfromeqn(y^2-89*(1-t^4))`.
`compute/global_boundary_quotients.gp` reproduces these calculations;
found point representatives may differ. These diagnostics are
**VERIFIED(PARI/GP 2.17.4)** and are not dependencies of the Tunnell
proof. The other four nontrivial characters have genus-zero quotients.

### A smooth proper model has no rational boundary points

**CITED (Tunnell, the four-square AP theorem, and surface resolution).**
Let Y be the selected covering open over U. There exists a smooth proper
compactification Ybar, isomorphic to Y over U, such that

\[
                         (\overline Y\setminus Y)(\mathbb Q)=\varnothing.
\]

Here is a model construction that also controls exceptional fibers.
Let X be the projective closure of V in P^8 with homogeneous root
coordinates [e:r_(a,b)]. Normalize X in the degree-eight function field
of Y, then resolve the resulting projective surface, preserving its
smooth open Y. Finiteness of normalization for varieties and resolution
of surfaces over Q are the classical geometric inputs; see
[Stacks, resolution of surfaces](https://stacks.math.columbia.edu/tag/0BGP).
This supplies a morphism pi:Ybar->X. No explicit blowup sequence is needed
for the rational-image exclusion, but one may be needed to compute classes.

For any rational point of Ybar its image on X is rational. The image is
accounted for by the following exhaustive alternatives:

1. **e=0:** the opposite-root identities
   r_(a,b)^2+r_(-a,-b)^2=2e^2 force all eight roots to vanish over R,
   which is not a projective point.
2. **A zero entry with e!=0:** clear rational root denominators and divide
   their common gcd. The mod-4 proof of F4.1 uses no distinctness assumption
   and forces all nine primitive roots odd. Thus no entry can be zero.
3. **e!=0 and a distinctness line:** normalize e=1. Six lines are excluded
   except at all-equal configurations by the four-square AP theorem, as
   in GB.7. All signed all-equal fibers are excluded by the twist classes.
   The v=0 axis is excluded in GB.7; GB.8 excludes the u=0 axis.
4. **The image lies in U:** the cover is finite etale and smooth there.
   Normalization and the chosen resolution preserve it, so the point
   lies in Y, not in its boundary.

In case 3 normalization cannot introduce a rational lift invisible to
the affine root-sum equations. Each z_i satisfies the monic integral
equation z_i^2=(r_j+r_k)/d_i over V, so is a regular function on the
finite normalization above V and on its resolution. At a rational point
its value is rational and must satisfy those same equations. This
argument covers singular fibers and exceptional divisors over them.

The selected Y is still everywhere locally soluble, with genuine adeles
as in GB.7. Its absence of rational boundary points removes the specific
rational-boundary explanation of GB.3 for this twist. It does **not**
show Y(Q) is empty, nor that a finite Brauer obstruction exists.

### Concrete starting model for the next investigation

Put s_i=q_i z_i^2, q=(17,89,1513), and eliminate the three row roots:

\[
 A=s_1-s_2+s_3,\quad B=s_1+s_2-s_3,\quad C=-s_1+s_2+s_3.
\]

The row conditions become the explicit affine quartic surface

\[
              3(s_1^2+s_2^2+s_3^2)-2(s_1s_2+s_2s_3+s_3s_1)=3.
\]

Every point of Y maps to this surface, with u=A^2-1, v=B^2-1.
To recover Y one must also retain five further square conditions:

\[
 2-A^2,\quad 2-B^2,\quad 2-C^2,\quad
 1+A^2-B^2,\quad 1-A^2+B^2,
\]

and all nonzero/distinctness conditions. Dropping these square conditions
only enlarges the target. A class found on the row quartic must be tested
after their pullback; GB.1 warns that pullback can split a symbol.

The row model remains a candidate for a fibration or Brauer calculation,
with nontriviality checked after restoring the five square roots. The
owner subsequently prioritized the universal family: UT.2--UT.4 in the
companion note now give a necessary reduction and reject local forcing
of q_3=q_1q_2. Further class calculations should track the general twist
parameters. Neither this chosen twist nor q_3=q_1q_2 is known to be forced
by an MSS3.

## Reproduction and evidence boundaries

```text
python -m compute.global_obstruction_probe
python -m compute.global_obstruction_probe --ap-bound 100
python -m compute.global_obstruction_probe --boundary-certificate
python -m verify --only gb.
python -m verify --fast --only a5.
python -m verify --fast --only f5.
python -m verify --only gauntlet
```

The gb checks verify the explicit matrix algebra, radicand bookkeeping,
Jacobian ranks, rational lift controls, 95-prime fourth-root controls,
56 conic identities, 70 four-line subsets, triangle sign fibers, the
all-prime square-character certificate, AP boundary reductions, complete
Tunnell counts for 89, the quotient map and its exceptional fibers, and
the projective-boundary bookkeeping.
They do not implement a Brauer-group algorithm, prove the imported
arithmetic theorems, compute the rational points on Y, or establish an MSS3
impossibility claim. No new obstruction predicate is registered because
this checkpoint asserts no obstruction to any anchor or MSS3.

## Sources and provenance

- Tunnell, *A Classical Diophantine Problem and Modular Forms of Weight
  3/2*, Invent. Math. 72 (1983), 323--334,
  [original paper scan](https://sites.math.rutgers.edu/~zeilberg/EM22/JT1983.pdf).
  **READ, relevant portions only, 2026-09-10:** printed pp.323--325
  (PDF pages 2--4), visually inspected from the scan. The theorem on
  p.323 is unconditional in the needed direction; p.325 gives the exact
  ternary-form count. The modular-form proof is CITED, not reproduced.
- PARI/GP [elliptic-curve manual](https://pari.math.u-bordeaux.fr/dochtml/ref-stable/Elliptic_curves.html),
  `ellfromeqn`, `ellrank`, `elltors`: **READ relevant entries**. The
  diagnostic run used installed version 2.17.4; GB.8 does not depend on it.
- Stacks Project, [Theorem 54.14.5](https://stacks.math.columbia.edu/tag/0BGP)
  and [introduction to surface resolution](https://stacks.math.columbia.edu/tag/0ADX):
  **READ statements/context**. Existence of resolution is CITED; no
  explicit surface resolution or Brauer-group calculation is claimed.
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
