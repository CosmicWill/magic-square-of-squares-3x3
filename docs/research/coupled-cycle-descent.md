# Coupled even-cycle descent and its boundary

2026-09-11. Independent branch `research/proof-alternatives`, continuing
[UT.1--UT.4](universal-twist-reduction.md) at checkpoint dd21402.

This gives a universal four-parameter cover family whose prime support
depends only on the primitive offset direction. It also proves that an
infinite subfamily has smooth rational boundary points. Thus a uniform
exclusion by unrestricted finite Brauer tests on these covers cannot
finish the problem. Canonical local restrictions, further descent, and
the rational interior remain unresolved. No MSS3 exclusion is claimed.

## Notation

Use UT's primitive integer roots, center m>0, offsets U=Gk,V=Gl, with
gcd(k,l)=gcd(m,G)=1. Label the root grid

\[
 \begin{pmatrix}a&b&c\\d&m&f\\g&h&i\end{pmatrix}.
\]

The corresponding squares are the Lucas grid in UT. The four frames
are (a,b,c), (g,h,i), (a,d,g), (c,f,i), in that order. On a frame put

\[
 T(x,y,z)=\frac{(x+y)(y+z)(z+x)}{8m^3},\qquad
 (T_0,T_1,T_2,T_3)=(T(a,b,c),T(g,h,i),T(a,d,g),T(c,f,i)).
\]

On the admissible surface all these factors are nonzero. Define

\[
 F_1=T_0T_1,\quad F_2=T_2T_3,\quad F_3=T_0T_2,\qquad
 F_4=C=\frac{ai+cg}{2m^2}.
\]

The four covers are imposed simultaneously:

\[
                       \kappa_j Z_j^2=F_j\quad(1\leq j\leq4).
\]

All nine original square conditions remain in the base. These equations
do not replace them by conditions solely on the three-root row quartic.

## CC.1. A universal family independent of the center's prime support

**PROVEN.** After the canonical root signs r=m mod 4 are chosen, every
hypothetical MSS3 lifts to the displayed cover with signed odd squarefree
integer labels satisfying

\[
                 \kappa_j\equiv1\pmod8,\qquad Z_j\in\mathbb Z_2^\times.
\]

Write

\[
 P=(2k+l)(k+2l)(k-l),\qquad Q=(2k-l)(k-2l)(k+l).
\]

The prime supports of the labels satisfy

| Label | Allowed prime support |
|---|---|
| kappa_1 | P |
| kappa_2 | Q |
| kappa_3 | PQ |
| kappa_4 | (k-l)(k+l) |

Moreover gcd(|kappa_1|,|kappa_2|) divides 5. For a fixed primitive
direction these are finitely many labels, independently of both m and G.
The rational direction (k:l) is still unbounded.

### Why even cycles cancel m and G

Join two of the eight noncentral root positions when they occur together
in one frame. This graph has eight vertices, twelve edges and five
independent cycles: the four frame triangles and the corner cycle
(a,c,i,g). Its cycle space over F_2 has dimension 12-8+1=5. Restricting
to cycles with an even total number of edges gives dimension four.
A basis consists of the unions of frames (0,1), (2,3), (0,2), and the
corner cycle. Symmetric difference of edge sets corresponds to multiplying
the functions modulo squares. CC.2 identifies the corner product with C.

Here is the prime-support argument for any of these even cycles, including
unions of cycles. Put b_xy=(x+y)/2. Canonical signs make each b_xy odd.
The product of the normalized edge slots is prod(b_xy)/m^e; e is even,
so the center denominator is a square. At an odd prime p outside the
primitive differences ell_xy=(x^2-y^2)/G of the selected edges:

* If p does not divide G, all these entry differences are units, so no
  corresponding root sum is divisible by p. This includes p dividing m.
* If p divides G, it does not divide m, and every root is +m or -m mod p.
  A sum vanishes precisely on an edge crossing these two sign groups.
  Its complementary difference is a unit, so its valuation is v_p(G).
  Every cut of an even-degree graph has even size: summing vertex degrees
  on one side counts internal edges twice and cut edges once. The total
  valuation is consequently even.

Thus only primitive-direction primes can enter the square class. The
selected edge differences give exactly the supports in the table.
For the first two rows, determinants between their primitive linear
factors have absolute values 1,2,4,5. A prime common to one factor of P
and one of Q therefore divides 2 or 5, since gcd(k,l)=1. The labels are
odd, which proves the asserted gcd restriction. No conclusion that a
label divides the *squarefree part* of the displayed polynomial is used;
even valuations can split between a root sum and its complementary
difference when both roots vanish modulo a direction prime.

### The simultaneous condition at 2

Normalize m=1 locally and write u=8x,v=8y, with x,y in Z_2. The square
root of 1+8t that is 1 mod 4 satisfies

\[
                 r(t)=1+4t-8t^2\pmod {16}.
\]

For a frame with offset parameters t_1+t_2+t_3=0, expanding its three
half-sums gives

\[
 T\equiv1+4(t_1t_2+t_2t_3+t_3t_1)\pmod8.
\]

The four frames therefore all have the same residue

\[
                   T_j\equiv1+4(x^2+xy+y^2)\pmod8.
\]

Their pairwise products are 1 mod 8. Also r(t)r(-t)=1 mod 16, so both
normalized opposite-corner products are 1 mod 16 and C=1 mod 8.
All four slots are units, proving the canonical label and lift conditions.

Conversely, every four-tuple of odd labels that are 1 mod 8 has full
canonical admissible local lifts at 2. Take sufficiently small generic
u,v in 8Z_2, select all eight roots 1 mod 4, and apply the identities
above. Each F_j/kappa_j is 1 mod 8 and has a square root. Nonzero and
distinct entries are obtained by avoiding the finitely many direction
lines. This is a local statement and imposes no global prime support.

## CC.2. The corner identity, degree, and a local counterexample

**PROVEN.** Set S=a+c+i+g and
P_c=(a+c)(c+i)(i+g)(g+a). The opposite-pair equations give

\[
 a^2+i^2=c^2+g^2=2m^2,\qquad
                    P_c=\frac{S^2(ai+cg)}2.
\]

For a direct verification put A=a+i, B=a-i, D=c+g, E=c-g.
Then B^2=4m^2-A^2, E^2=4m^2-D^2, and expanding the two opposite
products gives

\[
 P_c=\frac{((A+D)^2-B^2-E^2)^2-4B^2E^2}{16}
     =\frac{(A+D)^2(A^2+D^2-4m^2)}4.
\]

This is the claimed identity. In particular

\[
 \frac{P_c}{16m^4}=C\left(\frac{S}{4m}\right)^2.
\]

All factors are nonzero on the admissible domain; if S were zero, the
identity would force P_c=0. Also C=0 implies U^2=V^2 and is excluded.
Thus the corner-edge product and C have exactly the same square class.

### The simultaneous cover has geometric degree 16

**PROVEN.** The four functions F_j are independent modulo squares over
the algebraic closure of the original surface's function field. The
following valuation rows are available on generic direction-line
divisors of the full square surface:

| Direction line | Opposite signs on the indicated equal-root pair(s) | Orders of F_1,F_2,F_3,F_4 modulo 2 |
|---|---|---|
| u=-2v | top pair only | 1,0,1,0 |
| u=-2v | bottom pair only | 1,0,0,0 |
| u=2v | left pair only | 0,1,1,0 |
| u=v | top corner pair only | 1,0,1,1 |

For example u=-2v makes b^2=c^2 and g^2=h^2. Their signs are
independent over the algebraic closure. All other entry radicands are
nonzero at a generic point of that line. A root sum for an opposite-signed
equal pair has a simple zero: its product with the complementary unit
difference is the corresponding linear entry difference. The same argument
applies to the other rows. This produces the stated valuations; the
corner identity permits use of its four-edge product in the last column.
The four rows have rank four over F_2. Any nonempty product of the F_j
therefore has an odd valuation somewhere and cannot be a square.
Consequently every simultaneous twist is geometrically integral of degree
16 and is etale over the original admissible surface.

### Signs cannot force the corner label to be trivial

**PROVEN.** There is a full admissible Q_97 grid for which every root-sign
choice, and hence every D4 choice, has a nonsquare corner label.
Use u=23,v=26, center 1, and these root seeds modulo 97:

\[
 \begin{pmatrix}86&90&67\\95&1&80\\84&70&50\end{pmatrix}.
\]

The nine exact radicands are 24,-48,27,4,1,-2,-25,50,-22. They are
distinct nonzero squares modulo 97, and every seed has unit derivative
2r. They thus lift to an admissible Q_97 point to all precisions.
This is not a rational solution; the exact negative entries make that
distinction explicit.

The opposite-corner products are 32 and 2 modulo 97. The sixteen corner
sign choices give C in {17,80,15,82}, each a nonsquare (its 48th power
is 96). D4 only permutes the opposite pairs. Equivalently the full corner
product sign orbit is

\[
                 [\pm C],\quad[\pm C(u^2-v^2)],
\]

and -1 and u^2-v^2=47 mod 97 are both squares. This rules out a local
or characteristic-zero identity forcing the fourth label to 1. It does
not refute a potential additional theorem restricted to rational points.

## CC.3. The single corner cover always has rational boundary

**PROVEN.** For every nonzero rational kappa, the single double cover
kappa*z^2=C has a smooth birational model containing a rational boundary
point. Its support restriction alone does not remove the boundary.

Normalize m=1 and put r=ai,s=cg. Then

\[
                 2(r-s)C=v^2-u^2.
\]

At the signed all-equal point with g=-1 and every other root +1, r=1,
s=-1 and C=0. The raw point z=0 is singular; it cannot simply be counted
as a smooth rational point. Blow up using u=t,v=tw,z=tZ. In the open
chart r-s!=0 the strict-transform equation is

\[
                  2\kappa(r-s)Z^2=w^2-1.
\]

At t=0,w=1,Z=0 and the specified root signs this is a rational point.
The entry-root derivatives 2r_j are nonzero and the new equation has
w-derivative -2, so the point is smooth on the two-dimensional model.
The chart agrees with the original cover for t!=0. Its exceptional curve
is w^2-4*kappa*Z^2=1, with a rational point for every kappa. This is an
explicit normalization/blowup audit, not an inference from the raw node.

## CC.4. Infinitely many simultaneous universal twists retain boundary

**PROVEN.** Even the simultaneous degree-16 cover has smooth rational
boundary for an infinite collection of label tuples permitted by CC.1.

For w a positive multiple of 8, specialize the all-equal root signs to

\[
                 (-1,-1,-1,-1,1,1,-1,1,1)
\]

in row-major order and approach along u=t,v=tw. The four slots have
orders (2,2,0,2) in t and leading coefficients

\[
 L_1=-\frac{(w-1)(2w+1)}{16},\quad
 L_2=-\frac{(w+1)(2w-1)}{16},\quad L_3=1,\quad
 L_4=-\frac{w^2-1}{4}.
\]

To verify these expressions, the top and left frame products have
constant term -1, whereas the bottom and right frame products begin
with (w-1)(2w+1)t^2/16 and (w+1)(2w-1)t^2/16. The identity in CC.3
gives the last coefficient, now with r=-1,s=1.

Choose kappa_j=sqclass(L_j). These are all 1 mod 8, since w=0 mod 8,
and obey the primitive-direction support constraints with (k,l)=(1,w).
After substituting Z_j=t^(order_j/2)X_j, the equations at t=0 have
nonzero rational X_j. Their derivatives 2*kappa_j*X_j are nonzero.
The rescaled slots are regular: for every root sum vanishing at t=0,

\[
                 (r_i+r_j)/t=\ell_{ij}(w)/(r_i-r_j),
\]

whose denominator is a unit. For C use the identity from CC.3. Hence
the rescaled equations define a smooth chart with a rational point,
birational to the full cover, rather than just a formal leading solution.

An explicit example is

\[
 (k,l)=(1,8),\qquad (\kappa_1,\kappa_2,\kappa_3,\kappa_4)
      =(-119,-15,1,-7),\qquad
                 (X_1,X_2,X_3,X_4)=(1/4,3/4,1,3/2).
\]

The boundary family has infinitely many numerical label tuples, not only
infinitely many directions. Given any finite prime set, choose an odd
prime p outside it. The Chinese remainder theorem permits w=0 mod 8
and w=1+p mod p^2, with w positive. Then p occurs oddly in w^2-1 and
therefore in kappa_4. No fixed finite prime support suffices for this family.

**CITED DEDUCTION, using [GB.3](global-obstructions.md).** For each of these
twists, and for every
finite subgroup B of the Brauer group of its admissible open, the
unrestricted adelic Brauer set is nonempty. The proof of GB.3 applies
to the smooth geometrically integral chart with a rational boundary
point just constructed: classes extending to the smooth model are
locally constant near that point; Harari's formal lemma handles the
remaining finite classes. The almost-all-prime integral argument is
the same as in GB.3. The cited input is the formal lemma, not the
explicit chart or the elementary prime-support calculation.

This does **not** prove nonemptiness after imposing canonical root signs
and unit lift coordinates at 2, or another justified integral restriction.
The displayed rational boundary signs are mixed and are not canonical at
2. Although CC.1 supplies canonical local points at 2 for these labels,
the compatibility of that local condition with a finite Brauer set has
not been established. A rational boundary point can defeat a proposed
obstruction to existence while leaving an obstruction to specified local
conditions open. Neither kind of obstruction has been computed here.

The later [finite-descent audit](finite-descent-barrier.md) settles the
canonical-domain limitation for finite groups generated by symbols with
twist constants in their first slots. Arbitrary Brauer classes on these
individual nontrivial twists remain uncomputed. The same audit proves a
general surviving-*some*-twist result, including canonical roots at 2.

## Consequences for the proof search

The center-independent four-parameter reduction is universal. Its
direction parameter is unbounded, and simply excluding numerical twists
cannot establish impossibility. The 97-adic example prevents eliminating
the corner parameter by signs. The boundary family prevents a uniform
unrestricted finite-Brauer exclusion of all the covers in CC.1.

The finite-descent audit changes the next target to an arithmetic
exclusion of the surviving branch, a genuine decreasing-integer descent,
or another independently justified global restriction. Merely retaining
the canonical domain at 2 or adding a finite cover cannot complete the
finite-Brauer template. Any individual Brauer calculation must still
survive all original and cycle square roots and include its ramification
and local-domain audits. An obstruction solely on a quotient is insufficient.

For fixed direction, these even-cycle covers are also candidates for
descent on the complete direction fiber. No Jacobian image, Selmer
computation, or completeness theorem for those fibers is asserted here.

## Reproduction and scope of verification

```text
python -m compute.coupled_cycle_probe
python -m verify --only cce.
python -m verify --only ut.
python -m verify --only gb.
python -m verify --only gauntlet
```

The checks cover the graph cycle space, the valuation-rank certificate,
the exhaustive canonical residues modulo 32, exact corner identities,
bounded rational degenerate controls, the complete 97 residue certificate,
and explicit rescaled boundary charts. Bounded controls are not universal
exclusions. The written proofs supply the universal algebra and lifts;
the GB.3 formal-lemma deduction retains its CITED status. No new external
arithmetic theorem, campaign result, or headline impossibility predicate
is introduced.
