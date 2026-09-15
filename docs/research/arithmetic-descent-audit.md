# Arithmetic descent from the smaller corner integer

2026-09-14. Branch `research/proof-alternatives`, following checkpoint
7ab300b and the final section of [the finite-descent audit](finite-descent-barrier.md).

The corner-label-1 branch has an exact divisor parametrization. It retains
five square tests: the center and all four side entries. A separate
calculation shows why linear recombinations of the roots cannot turn the
smaller integer into a new shape. A quadratic numerator divided by a
linear denominator reduces projectively to a linear formula.

These results constrain proposed constructions. They do not exclude a
rational point, bound the remaining twist labels, or provide a descent.
All labels below are local to this note.

## AD.1. An exact divisor model with the side conditions retained

**PROVEN.** Use the root grid

\[
 \begin{pmatrix}a&b&c\\d&m&f\\g&h&i\end{pmatrix},\qquad m>0,
\]

with squared entries given by the Lucas grid, offsets U,V, primitive
integer roots, and canonical root signs modulo 4. Suppose kappa_4=1.
The previous audit gives a positive odd integer

\[
 n^2=(ai+cg)/2,\qquad 0<n<m
\]

for an admissible grid. Its half-sums obey

\[
 x^2=n^2+w^2,\quad z^2=n^2+y^2,\quad m^2=n^2+y^2+w^2,
 \qquad U=2xy,\ V=2zw.
\]

Here x=(a+i)/2, y=(a-i)/2, z=(c+g)/2, w=(c-g)/2.
Replace them by magnitudes when constructing the divisor model: x,z>0
and y,w>=0. This replaces U,V by their magnitudes; independent sign
changes of the offsets permute the nine Lucas entries. Thus all square,
positivity and distinctness tests are preserved. The original orientation
and canonical signs can be restored after reconstruction.

Set r=x-w and s=z-y. Since

\[
 (x-w)(x+w)=(z-y)(z+y)=n^2,
\]

the complete possibilities are positive odd divisors

\[
 r\mid n^2,\quad s\mid n^2,\quad r,s\le n,
\]

and conversely they give integer half-sums

\[
 x=\frac{n^2+r^2}{2r},\quad w=\frac{n^2-r^2}{2r},\qquad
 z=\frac{n^2+s^2}{2s},\quad y=\frac{n^2-s^2}{2s}.
\]

The quantities x,z are odd and y,w are multiples of 4, since
n^2/r is congruent to r modulo 8, and likewise for s. Define

\[
 M=n^2+y^2+w^2,\quad U=2xy,\quad V=2zw.
\]

The five remaining requirements are exactly

\[
 M=m^2,\quad M-U-V=b^2,\quad M-U+V=d^2,
 \quad M+U-V=f^2,\quad M+U+V=h^2.
\]

The four corner roots are already

\[
             (a,c,g,i)=(x+y,z+w,z-w,x-y).
\]

Require positivity and pairwise distinctness of all nine entries, and
gcd(n,y,w)=1. These conditions are both necessary and sufficient to
reconstruct a primitive admissible integer grid in this branch, up to
the symmetries just described. Necessity of the gcd condition follows
because a prime dividing n,y,w divides x,z,m and all nine roots.
Conversely, an odd prime dividing all roots divides x,y,z,w, hence n;
all roots are odd, so there is no factor 2. Choosing canonical signs
changes a,i together and c,g together, since y,w are multiples of 4;
it therefore preserves ai+cg=2n^2.

### The retained equations in divisor coordinates

Put K=(r^2+s^2)(n^4+r^2s^2). Direct expansion gives

\[
 4r^2s^2M=K,\qquad
 U+V=\frac{n^4-r^2s^2}{rs},\qquad
 U-V=\frac{n^2(r^2-s^2)}{rs}.
\]

Thus the five square tests can equivalently be written

\[
\begin{aligned}
 (2rsm)^2&=K,\\
 (2rsb)^2&=K-4rs(n^4-r^2s^2),\\
 (2rsh)^2&=K+4rs(n^4-r^2s^2),\\
 (2rsd)^2&=K-4rsn^2(r^2-s^2),\\
 (2rsf)^2&=K+4rsn^2(r^2-s^2).
\end{aligned}
\]

For the stated divisor inputs, the unscaled targets are integers; a
rational square equal to an integer has an integer square root. The
scaled equations therefore lose no integrality condition.

For each fixed n the divisor list is finite, even though n remains
unbounded. Also

\[
  y,w\le(n^2-1)/2,\qquad 2m^2\le n^4+1.
\]

These are size bounds, not a transformation to a smaller solution.
The cases r=n or s=n give a zero offset and must be retained as
degenerate controls; r=s gives U=V. Other coincidences are rejected by
the full distinctness test.

### A positive control for the missing four squares

For n=399, r=147, s=19 the model gives

\[
 (x,y,z,w,m)=(615,4180,4199,468,4225),
 \qquad (a,c,g,i)=(4795,4667,3731,-3565).
\]

The nine Lucas entries are positive, distinct and magic. The center and
corners are squares, with (ai+cg)/2=399^2. The four side entries are

\[
             8778961,\quad16639489,\quad19061761,\quad26922289,
\]

and none is a square. This verifies why the corner parametrization
alone cannot supply the missing grid. It is not an MSS3 example or an
exclusion of all divisor inputs.

## AD.2. A linear formula centered at n has constant shape

**PROVEN.** Let R=(a,b,c,d,m,f,g,h,i), and work on the cone defined by
the six original magic-square quadrics and ai+cg=2n^2. Suppose nine
homogeneous linear forms in (R,n), with rational coefficients and
center form n, satisfy the full target magic-square equations as
identities on this cone. Then every output root is c_j*n for a rational
constant c_j. In particular the resulting projective grid is independent
of the input.

*Proof.* At n=0 take m=1 and all eight other roots independently in
{+1,-1}, subject to ai=-cg. There are 128 such real points, all full
square grids. Let S be their 128-by-9 root matrix. Its exact Gram matrix
is

\[
                         S^{\mathsf T}S=128I_9.
\]

Indeed the constraint fixes a product of four signs; all first and
second moments of distinct noncentral signs still vanish. The center
column is constant 1. This also gives a direct rank-nine certificate.

For each output opposite pair, the target identity is L_j^2+L_{8-j}^2
=2n^2. At every listed real n=0 point both outputs vanish. Write
L_j=ell_j(R)+c_j*n. The rank certificate forces ell_j=0, proving the
claim. The center has the asserted form already.

**Constant shape does not mean all entries equal.** The constants must
themselves satisfy the nine-square magic equations with center 1.
Unequal degenerate constant grids exist. If a nondegenerate rational
constant grid existed, it would already solve the original problem;
the argument does not rule one out. It says that a linear formula cannot
construct a new shape from its input.

For example, scaling the AP root grid
(5,-7,1,1,5,-7,-7,1,5) by n/5 gives rational center n for any n.
Clearing denominators and dividing the common root gcd always restores
primitive center 5. The apparent factor n/5 is not an arithmetic descent.

## AD.3. Quadratic numerators also lose the proposed scale factor

**PROVEN, with an exact finite linear-algebra certificate.** Suppose the
output roots L_j are homogeneous quadratics in (R,n), the center is nD
for a homogeneous linear form D, and the target magic equations hold
identically on the same cone. Then, modulo its defining quadrics,

\[
                        L_j=nM_j
\]

for homogeneous linear forms M_j. These M_j satisfy the target magic
equations with center D. The nontrivial square class in CC.2 makes the
corner cover geometrically integral, so identities on n!=0 extend to
the cone. In particular:

- With center n^2, every output is c_j*n^2; the projective shape is constant.
- A formula with quadratic numerators and common linear denominator D,
  producing rational center n, has the same projective image as the
  linear grid (M_j). Primitive integer normalization cancels the common
  factor n/D. A further decrease from normalization would require its
  own proof; the size n<m supplies none by itself.

*Boundary certificate.* Consider all 384 real algebraic grids obtained
by taking m=10, (U,V)=(0,0),(10,10),(10,-10), and the 128 sign patterns
from AD.2 at each seed. Their positive magnitudes belong to

\[
                   \mathbb Q(\sqrt2,\sqrt3,\sqrt5,\sqrt{11}).
\]

They satisfy the six magic quadrics and ai+cg=0 exactly. Evaluate the
45 monomials R_j R_k, j<=k, and expand in the 16 independent squarefree
radical basis elements. After deduplication there are 284 rational rows.
Exact rational elimination gives rank 38. The kernel has dimension seven
and is exactly the span of the six original magic quadrics and ai+cg:
all seven vanish on every row and their coefficient vectors have rank seven.

These are exact evaluations at specified algebraic points, not a sample
used to infer a general zero set. Their kernel is an upper bound for
any quadratic vanishing on the entire real n=0 boundary; the seven
displayed quadrics attain that bound. The code uses integer radical
arithmetic and rational elimination, without numerical square roots or
an optional computer algebra system.

*Proof of the assertion.* The target opposite-pair identities imply that
every L_j vanishes at those real n=0 points. Write
L_j=L_{j,0}(R)+n*ell_j(R)+c_j*n^2. The certificate places L_{j,0} in
the seven-dimensional kernel. On the cone the six old quadrics vanish
and ai+cg=2n^2. Thus L_j=nM_j. Cancelling n^2 in the target equations
on n!=0 gives the asserted linear grid. For D=n apply AD.2.

### Scope of both restrictions

The hypotheses concern rational-coefficient polynomial identities on the
whole corner cover, or its dense admissible open. They do not assume
that rational admissible points are dense, and make no conclusion about
formulas valid only on an exceptional arithmetic subset. They also do
not treat extra root variables from the other cycle covers, higher-degree
numerators, arbitrary denominators, or correspondences with several
possible outputs. The use of real boundary points is essential to the
sum-of-two-squares step; it is not a finite-field or congruence obstruction.

## Remaining arithmetic task

**FAILED-ATTEMPT:** using n as a new center through homogeneous linear
root recombination, or its quadratic-over-linear extension, has not
produced a descent. The restrictions above explain its failure precisely.
They do not constitute a general theorem forbidding arithmetic descent.

The concrete input for further work is now the five retained square
equations of AD.1, together with r,s dividing n^2, primitivity, positivity
and distinctness. A nonlinear correspondence would have to preserve all
five tests, preserve a stated branch on which it can be iterated, and
strictly decrease the primitive integer invariant after denominator
clearing. Alternatively, a uniform exclusion of this divisor system
would handle kappa_4=1. Neither result is established. The other corner
labels remain unbounded and outside this case.

## Verification and source check

```text
python -m compute.arithmetic_descent_probe
python -m verify --only ard.
python -m verify --only fdb.
python -m verify --only cce.
python -m verify --only ut.
python -m verify --only gb.
python -m verify --only gauntlet
```

The six new checks verify the divisor identities, bounded AP round-trips,
the positive five-square control, both exact boundary matrices, and the
constant-shape/primitive-normalization distinction. The identity check
uses a 5-by-5-by-5 interpolation grid: each cleared residual has degree
at most four in each variable, so this is an exact polynomial certificate.
The AP count is a bounded control, not a classification.

Related primary source, **READ** 2026-09-14: Christian Wolird,
[*A New Transformation of the Magic Square of Squares*, arXiv:2310.12164v1,
sections 1--5](https://arxiv.org/html/2310.12164v1). Section 4 explicitly
computes the error preventing certain half-sum constructions from forming
new arithmetic grids. Its Gaussian constructions do not provide the
integer descent sought here. This observation is background only; none
of AD.1--AD.3 depends on the paper.
