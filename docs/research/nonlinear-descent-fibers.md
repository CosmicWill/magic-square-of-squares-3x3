# Nonlinear descent candidates and the full divisor fibers

2026-09-14. Branch `research/proof-alternatives`, following cc54456 and
[AD.1--AD.3](arithmetic-descent-audit.md).

Two natural nonlinear constructions fail to give a descent. Divisor
reciprocity preserves every square condition but is exactly a reflected
rescaling. Doubling a point on an elliptic quotient can lose even the
lift to the center quartic. More generally, the full curve at each
admissible rational divisor ratio has genus 129, so elliptic multiplication
cannot lift to a rational self-map of that curve.

The reciprocity and polynomial certificates are **PROVEN** here. Genus,
map-degree, and boundary-completeness conclusions below are explicitly
**CITED deductions**, with the imported ingredients identified. None
excludes a rational interior point or a new MSS3 class.

## ND.1. Reciprocity preserves the grid but not a smaller primitive center

**PROVEN.** Retain AD.1's variables, initially with positive n,r,s and
r,s dividing n^2. Extend the formulas rationally, without insisting that
the transformed half-differences stay positive. Put

\[
 n'=\frac{rs}{n},\qquad r'=r,\quad s'=s,
 \qquad \lambda=\frac{rs}{n^2}.
\]

Direct substitution in the four half-sum formulas gives

\[
 (x',y',z',w')=\lambda(z,-w,x,-y),\qquad
 (m'^2,U',V')=\lambda^2(m^2,-V,-U).
\]

Thus the complete root grid can be chosen as

\[
 \begin{pmatrix}a'&b'&c'\\d'&m'&f'\\g'&h'&i'\end{pmatrix}
 =\lambda
 \begin{pmatrix}g&h&i\\d&m&f\\a&b&c\end{pmatrix}.
\]

All five retained square equations, positivity, and distinctness are
preserved. Also ai+cg transforms by lambda^2, so the chosen corner
square root is n'=lambda*n. This is an involution on the rational
parameters. For r,s<=n with rs<n^2 it has n'<n and m'<m as rational
numbers.

Nevertheless, multiplying a rational root grid by a common nonzero
rational number does not change its primitive integer representative.
After clearing denominators and dividing the common root gcd, the output
is just the reflected input. The primitive center is unchanged. The
apparent decrease cannot be iterated as an integer descent.

For the earlier five-square control, (n,r,s)=(399,147,19) maps to
n'=7 with lambda=1/57. Its missing side squares remain missing. As a
full-square control, the AD model (n,r,s)=(3,1,3) has m=5 and maps to
n'=1, m'=5/3; primitive normalization restores m=5. The same phenomenon
is verified on 179 canonical primitive AP controls.

This calculation does not classify all nonlinear transformations. It
identifies this particular one exactly as a symmetry and a scale change.

## ND.2. The full curve at a fixed divisor ratio

**PROVEN, algebraic model.** Normalize s=1 projectively and put
k=r/s and t=n/s. The corresponding root grid is the old one divided by
s. Set A=k^2+1 and use five lift variables Y_m,Y_b,Y_d,Y_f,Y_h:

\[
\begin{aligned}
 Y_m^2=F_m(t)&=A(t^4+k^2),\\
 Y_b^2=F_b(t)&=(A-4k)t^4+k^2(A+4k),\\
 Y_d^2=F_d(t)&=A(t^4+k^2)-4k(k^2-1)t^2,\\
 Y_f^2=F_f(t)&=A(t^4+k^2)+4k(k^2-1)t^2,\\
 Y_h^2=F_h(t)&=(A+4k)t^4+k^2(A-4k).
\end{aligned}
\]

The five normalized roots are Y_j/(2k). The corners are reconstructed
from

\[
 x=\frac{t^2+k^2}{2k},\quad w=\frac{t^2-k^2}{2k},\qquad
 z=\frac{t^2+1}{2},\quad y=\frac{t^2-1}{2}
\]

as (a,c,g,i)=(x+y,z+w,z-w,x-y). Thus no side-square condition has
been dropped. Let C_k be the smooth projective model of the five
simultaneous square-root equations. Let E_k denote the center quartic
Y_m^2=F_m(t), with its smooth projective model.

An admissible AD.1 input has k>0 and k!=1; k=1 forces U=V. Its n,r,s
are odd, so k and t are 2-adic units. The curves C_k are defined over Q
and will also be considered without this last integral condition. Every
AD.1 candidate maps to one of them. Conversely a rational interior point
reconstructs a rational MSS3 with the displayed signed corner square;
the canonical-label-1 converse also requires the normalization conditions
of AD.1. Arbitrary choices of root signs must not silently be identified
with canonical signs.

Reciprocity on the model is the explicit involution

\[
 t\longmapsto k/t,\qquad
 (Y_m,Y_b,Y_d,Y_f,Y_h)\longmapsto
 \frac{k}{t^2}(Y_m,Y_h,Y_d,Y_f,Y_b).
\]

The reciprocal polynomial identities t^4 F_j(k/t)=k^2 F_{sigma(j)}(t)
also account for its action at zero and infinity on the proper curve.

### An elliptic quotient and a failed doubling lift

**PROVEN, explicit identities.** The center quartic has rational point
(t,Y_m)=(1,A), and maps to the nonsingular cubic

\[
 E_k^+ : Y^2=X^3+k^2A^2X,\qquad
                  (X,Y)=(At^2,AtY_m).
\]

The displayed substitution verifies the cubic equation directly. Its
generic fiber consists of (t,Y_m) and (-t,-Y_m). Rational lift-back
requires X/A to be a rational square, as well as the other four side
conditions on C_k.

The section (1,A) maps to P=(A,A^2). Applying the usual tangent formula
on the cubic gives

\[
 X([2]P)=\frac{(k^2-1)^2}{4},\qquad
 Y([2]P)=-\frac{(k^2-1)(k^4+6k^2+1)}8.
\]

At k=3 this is (10,100) -> (16,-136). Lifting the doubled point would
require t^2=8/5, which is not a rational square. The input section has
all five rational square lifts (see ND.5), so this is a full degenerate
grid control. It demonstrates that doubling on this quotient is not
automatically a transformation even of the center quartic. It does not
exclude another elliptic operation or an exceptional arithmetic subset.

## ND.3. All nonexceptional rational fibers have genus 129

### Complete branch certificate

**PROVEN.** For every rational k outside {0,1,-1}, all five displayed
quartics have degree four, are squarefree, and have pairwise disjoint
geometric root sets. The exact discriminants are

| Polynomial | Discriminant |
|---|---|
| F_m | 256 k^6 A^6 |
| F_b, F_h | 256 k^6 (A-4k)^3 (A+4k)^3 |
| F_d, F_f | 256 k^6 (k^2-3)^2 A^2 (3k^2-1)^2 |

Put B=(k^2-2k-1)(k^2+2k-1). All ten pairwise resultants are covered by

| Pair(s) | Resultant |
|---|---|
| (m,b), (m,h) | 4096 k^12 A^4 |
| (m,d), (m,f) | 256 k^8 (k^2-1)^4 A^4 |
| (b,h) | 65536 k^12 A^4 |
| (d,f) | 4096 k^8 (k^2-1)^4 A^4 |
| (b,d), (b,f), (h,d), (h,f) | 256 k^8 B^4 |

The additional quadratic factors have discriminants -4, 8 or 12, hence
no rational zeros. Thus 0,1,-1 are the entire rational exceptional set,
not merely the exceptions observed in a search. The leading coefficients
are covered by the same nonvanishing factors.

These identities are certified without optional algebra software. Every
quartic coefficient has degree at most four in k. The Sylvester
determinants have degree at most 32 in k; the determinants defining
discriminants have degree at most 28 before division by the leading
coefficient. Exact evaluations at the 33 integers k=2,...,34 therefore
prove all fifteen polynomial identities by interpolation. Fraction-free
integer determinants are recomputed on each check run.

### Connected cover and genus

**PROVEN, degree and branch structure.** Each square-root function has
four private simple zeros. No nonempty product of the five can be a
square in Qbar(t), the rational function field with algebraically closed
constant field. Hence C_k is geometrically
integral, has degree 32 over P1_t, and ramifies at exactly 20 points,
each with index two. Infinity is unramified: each polynomial has even
pole order four and a nonzero leading coefficient. The affine model is
smooth as well, since only one lift can vanish at a time and its
quartic has a simple root.

**CITED deduction from Riemann--Hurwitz:**

\[
                     2g(C_k)-2=-2\cdot32+20\cdot16=256,
                     \qquad g(C_k)=129.
\]

The same calculation for the center quartic gives genus one, and the
forgetful map pi:C_k -> E_k has degree 16. Its rational section at
t=1 supplies a choice of origin for E_k. These statements hold for
every rational k!=0,+/-1, including every admissible positive divisor
ratio, rather than just the generic parameter.

The imported formula and its hypotheses were checked in the
[Stacks Project, Section 53.12, especially Lemma 53.12.2](https://stacks.math.columbia.edu/tag/0C1B).
The exact branch calculation is internal; this note does not claim to
reprove the general curve theorem.

## ND.4. Elliptic multiplication cannot lift to a full fixed-ratio map

**CITED deduction.** Any nonconstant rational map C_k -> C_k has degree
one. More generally, a nonconstant rational map C_k -> C_l between any
two nonexceptional rational fibers has degree one.

Indeed a rational map between these smooth proper curves extends to a
morphism. In characteristic zero it is separable. If its degree is d,
Riemann--Hurwitz gives

\[
                         256=256d+\deg R,\qquad \deg R\ge0,
\]

so d=1. This applies on the proper model even when an affine formula
has denominators or omits finitely many points.

In particular suppose a rational map Phi:C_k -> C_k were to satisfy

\[
              \pi\circ\Phi=\alpha\circ\pi
\]

for an elliptic self-map alpha of degree greater than one. Multiplying
degrees gives 16*deg(Phi)=deg(alpha)*16, a contradiction. This includes
alpha(P)=[h]P+T for |h|>=2: translation has degree one and multiplication
has degree h^2. Doubling would force ramification degree -768. The
same obstruction applies to a degree-greater-than-one elliptic map
between two such fibers when the full maps and quotient maps commute.

A single rational self-map selecting an elliptic half would instead
obey [2] composed with pi composed with Phi = pi. Degrees would force
4*16*deg(Phi)=16, also impossible. This does not forbid a pointwise
arithmetic choice among several preimages; existence and rationality of
that choice would need a separate argument.

Imported inputs: extension of rational maps, [Stacks Project,
Lemma 53.2.2](https://stacks.math.columbia.edu/tag/0BXX); Riemann--Hurwitz
as above; degree of elliptic multiplication, [Andrew Sutherland,
MIT 18.783 Lecture 5, 14 February 2022, final slide](https://math.mit.edu/classes/18.783/2022/LectureSlides5.pdf#page=24).
All three were **READ** on 2026-09-14 and retain CITED status here.

This does not classify the degree-one automorphisms, prohibit a
correspondence with multiple outputs, or treat a rule that changes k
depending on the input point. Nor does it rule out an identity restricted
only to an exceptional set of rational points. High genus alone is not
a rational-point exclusion.

## ND.5. The rational boundary remains present and explicit

**PROVEN, sections.** Put B_+=k^2+2k-1 and B_-=k^2-2k-1. There are
32 independent choices of signs at each of the four t-values

\[
\begin{array}{c|ccccc}
 t&Y_m&Y_b&Y_d&Y_f&Y_h\\\hline
 +1,-1&A&B_+&B_-&B_+&B_-\\
 +k,-k&kA&kB_-&kB_-&kB_+&kB_+
\end{array}
\]

All values are nonzero for nonexceptional rational k. These give 128
distinct rational points of C_k. They reconstruct AP grids: U=0 at
t=+/-1, and V=0 at t=+/-k. They are necessary controls for any proposed
arithmetic exclusion.

**CITED deduction from the classical four-square AP theorem**
([F3 and its stated external quartic input](../foundations/F3-no-four-term-ap.md)):
these are exactly the rational points of C_k mapping to a degenerate
grid. This is not a determination of C_k(Q).

For completeness, the distinctness condition is

\[
 U V (U^2-V^2)(U^2-4V^2)(4U^2-V^2)\ne0.
\]

With rational roots and nonzero center, a zero entry is impossible:
its opposite would make 2m^2 a rational square. Center zero would force
every rational root to be zero and gives no projective point. All other
degeneracies beyond U=0 or V=0 have U=+/-V, U=+/-2V, or V=+/-2U.
They contain at least four distinct squares in arithmetic progression.
On the finite t-chart, U=0 gives t=+/-1 and V=0 gives t=+/-k; the other
factors t^2=-k^2 and t^2=-1 have no rational roots. At t=0 one has
U=V=-k/2. At infinity, after scaling the roots by t^-2, the limits are
m^2=A/(4k^2) and U=V=1/(2k). Thus zero and infinity supply no omitted
rational boundary points. The genus and complete-boundary arguments both
use the normalization, rather than discarding a coordinate pole.

As a different control, k=3,t=13 has five square-root seeds
(244,242,399,329,236) modulo 401, in order (m,b,d,f,h). They are units
and lift to arbitrary 401-adic precision. The reconstructed grid has
nine distinct nonzero entries modulo 401; the verification uses precision
401^8. This is a full local interior point, not a rational one.

## Verdict and next arithmetic target

**FAILED-ATTEMPT:** reciprocal divisor exchange gives no primitive
decrease, and quotient multiplication does not supply a full-grid map.
These failures are now certified. No uniform exclusion of AD.1 or of
any new MSS3 class has been obtained.

A further construction must do more than reflect/rescale or multiply
on the fixed-ratio elliptic quotient. Concrete possibilities still outside
the audit are a point-dependent change of divisor ratio, or a multivalued
arithmetic correspondence with a justified rational branch. Either must
preserve all five square tests, retain an iteratable domain, and decrease
the primitive invariant after clearing denominators. Another option is
to prove that the 128 boundary points exhaust the relevant rational
domain uniformly in k. No such proof or correspondence is known, and
the nontrivial canonical corner labels still need their own argument.

## Reproduction and verification scope

```text
python -m compute.nonlinear_descent_probe
python -m verify --only nlf.
python -m verify --only ard.
python -m verify --only fdb.
python -m verify --only cce.
python -m verify --only ut.
python -m verify --only gb.
python -m verify --only gauntlet
```

Seven checks cover exact reciprocity and primitive normalization, the
five retained equations under projective normalization, all fifteen
branch identities, their rational exceptional set, cover-degree and
genus bookkeeping, rational AP sections, the explicit failed doubling
lift, and the 401-adic full-fiber control. The checks do not reprove
Riemann--Hurwitz, multiplication degree, or the classical four-square
theorem, and do not enumerate rational interior points.
