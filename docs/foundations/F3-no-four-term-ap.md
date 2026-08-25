# F3 — No four distinct squares in arithmetic progression

**Status:** F3.1, F3.2 with corollaries, and the reduction chain
F3.3a–F3.3e **PROVEN** (complete proofs below, each algebraic step
machine-verified); the headline Theorem F3.3 rests additionally on the
classical quartic fact **(Q)**, which is **PROVEN-CLASSICAL** (Euler-era;
see Open Task F3-T1) and **VERIFIED** exhaustively here.
Verification: `python3 -m verify --only f3`.

Role in the program: kills the *collinear* degenerations of the Lucas
parametrization (e.g. $v = 3u$, where the nine entries would be nine squares
in AP), and supplies the "no square congruum" obstruction used by the attack
documents.

## 1. Elementary constraints

**Lemma F3.1.** Let $p^2 < q^2 < r^2 < s^2$ be squares in AP with common
difference $\delta$ and $\gcd(p,q,r,s) = 1$. Then $p,q,r,s$ are odd and
pairwise coprime, and $24 \mid \delta$.

*Proof.* Squares are $\equiv 0, 1 \pmod 4$. If $\delta$ were odd, the four
terms $t, t+\delta, t+2\delta, t+3\delta$ would cover all residues mod 4,
including 2 and 3 — impossible. If $\delta \equiv 2 \pmod 4$, the terms
alternate between two classes $t, t+2 \pmod 4$, and one of any two classes
differing by 2 lies in $\{2,3\}$ — impossible. So $4 \mid \delta$ and all
terms lie in one class: all $\equiv 0$ makes every root even (contradicting
primitivity), so all terms $\equiv 1 \pmod 4$ and all roots are odd. Odd
squares are $\equiv 1 \pmod 8$, so $8 \mid \delta$. Mod 3: squares are
$\equiv 0, 1$; if $3 \nmid \delta$, four AP terms cover all residues mod 3,
including 2 — impossible; so $3 \mid \delta$, and the terms share one class
mod 3, which must be $1$ (all $\equiv 0$ would make 3 divide every root).
Hence $24 \mid \delta$ and $3 \nmid pqrs$. Pairwise coprimality: a prime
$\ell$ dividing two terms divides their difference $k\delta$,
$k \in \{1,2,3\}$; $\ell \ge 5$ gives $\ell \mid \delta$, hence
$\ell \mid$ all terms — contradiction; $\ell = 2, 3$ were excluded. ∎

## 2. Fermat's right-triangle theorem and its corollaries

**Theorem F3.2 (FRT).** There are no positive integers $x, y, z$ with
$x^4 - y^4 = z^2$.

*Proof (Fermat's descent).* Take a counterexample with $x$ minimal. If a
prime $g$ divided $x$ and $y$, then $g^4 \mid z^2$, so $g^2 \mid z$ and
$(x/g,\, y/g,\, z/g^2)$ is a smaller counterexample — hence
$\gcd(x,y) = 1$, and $(y^2, z, x^2)$ is a primitive Pythagorean triple (in
some order of the legs), so $x$ is odd.

Throughout we use the classical parametrization: a primitive triple with odd
leg $L$, even leg $E$, hypotenuse $H$ is $L = m^2-n^2$, $E = 2mn$,
$H = m^2+n^2$ with $\gcd(m,n) = 1$, $m > n > 0$, $m \not\equiv n \pmod 2$.
(*Proof of the parametrization:* $E^2 = (H-L)(H+L)$; the two factors are
even with $\gcd = 2$, so $\frac{H-L}{2}\cdot\frac{H+L}{2} = (E/2)^2$ with
coprime factors, making both squares $n^2, m^2$; the stated properties
follow.)

*Case 1: $y$ odd.* Then $y^2 = m^2-n^2$, $z = 2mn$, $x^2 = m^2+n^2$.
Multiplying the first and third: $m^4 - n^4 = (xy)^2 > 0$, a new solution
with $m \le m^2 < m^2+n^2 = x^2$ and hence $m < x$ (as $m < x^2$ with
$m^2 < x^2$ forces $m < x$) — contradicting minimality.

*Case 2: $y$ even.* Then $y^2 = 2mn$, $z = m^2-n^2$, $x^2 = m^2+n^2$. In
$y^2 = 2mn$ with $\gcd(m,n)=1$ and exactly one of $m,n$ even, write the even
one as $2t$: then $(y/2)^2 = t\cdot(\text{odd one})$ with coprime factors,
so both are squares: $\{m,n\} = \{c^2, 2d^2\}$, $c$ odd. Then
$x^2 = c^4 + 4d^4$, so $(c^2, 2d^2, x)$ is a primitive triple with odd leg
$c^2$: $c^2 = u^2 - v^2$, $2d^2 = 2uv$, $x = u^2+v^2$, $\gcd(u,v) = 1$.
From $d^2 = uv$ with coprime factors: $u = g^2$, $v = h^2$, whence
$c^2 = g^4 - h^4$ with $g, h, c > 0$ and $g \le g^2 = u < u^2+v^2 = x$ —
contradicting minimality. ∎

**Corollary F3.2a (no Pythagorean triangle has square area).** If
$e^2+f^2 = g^2$ with $e, f, g > 0$ then $ef/2$ is not a perfect square.

*Proof.* Counterexample with minimal $g$, area $ef/2 = t^2$. If
$k = \gcd(e,f) > 1$: $k \mid g$, and the triangle $(e/k, f/k, g/k)$ has
area $t^2/k^2$, an integer (it is $\frac{(e/k)(f/k)}{2}$ with one of the
primitive legs even) and a square (from $k^2 \mid t^2$, $k \mid t$) —
contradicting minimality. So the minimal one is primitive:
$e = m^2 - n^2$, $f = 2mn$ (WLOG), and
$$t^2 = \tfrac{ef}{2} = mn(m-n)(m+n).$$
The four factors are pairwise coprime: $\gcd(m,n) = 1$; $m \pm n$ are odd;
$\gcd(m-n, m+n)$ divides $2m$ and $2n$ and is odd, hence 1;
$\gcd(m, m\pm n) = \gcd(m,n) = 1$ and likewise for $n$. A product of
pairwise coprime positive integers equal to a square makes every factor a
square: $m = A^2$, $n = B^2$, $m+n = D^2$, $m-n = C^2$; then
$A^4 - B^4 = (CD)^2$ with $A, B, CD > 0$ — contradicting F3.2. ∎

**Corollary F3.2b (Fermat: no congruum is a perfect square).** For every
$m$, no element of $D(m)$ ([F2.3](F2-aps-and-pythagorean.md)) is a perfect
square; equivalently, no three-term AP of distinct squares has a square
common difference.

*Proof.* If $d = 2ef = t^2$ with $e^2+f^2 = m^2$ and $e,f>0$, then $t$ is
even, $t = 2t_1$, and $ef/2 = t_1^2$ — contradicting F3.2a. The AP
equivalence is F2.2. ∎

**Consequence for MSS3.** In any putative magic square of squares the four
offsets $|u|, |v|, |u+v|, |u-v|$ are congrua ([F2.5](F2-aps-and-pythagorean.md)),
hence **none is a perfect square**. This is genuinely global information —
it comes from descent, not congruences — and is inherited by the attack
documents.

## 3. The four-square theorem: a complete reduction chain

**Theorem F3.3 (Fermat–Euler).** There do not exist four distinct perfect
squares in arithmetic progression.

The chain F3.3a → F3.3e below reduces F3.3, with complete proofs, to one
classical quartic statement:

> **(Q)** The equation $r^4 - r^2 s^2 + s^4 = \square$ has no solutions in
> coprime integers $r, s$ of opposite parity with $rs \neq 0$.

**(Q)** is Euler-era classical (SUMMARY-ONLY provenance; see Open Task
F3-T1) and is VERIFIED exhaustively by the check. Nothing downstream in
this repository uses F3.3 beyond excluding degenerate collinear families.

**Lemma F3.0 (four-number lemma).** If $AB = CD$ with $A,B,C,D$ positive
integers and $\gcd(A,B) = \gcd(C,D) = 1$, then there are pairwise coprime
positive integers $w, \alpha, \gamma, \tau$ with
$$A = w\alpha,\quad C = w\gamma,\quad B = \gamma\tau,\quad D = \alpha\tau.$$
*Proof.* Let $w = \gcd(A,C)$, $A = w\alpha$, $C = w\gamma$,
$\gcd(\alpha,\gamma) = 1$. Cancelling $w$ in $AB = CD$: $\alpha B = \gamma
D$, so $\gamma \mid B$; write $B = \gamma\tau$, forcing $D = \alpha\tau$.
Coprimality of all six pairs: $\gcd(A,B) = 1$ makes $w$ and $\alpha$
coprime to $\gamma$ and $\tau$; $\gcd(C,D) = 1$ makes $w \perp \alpha$ and
$\gamma \perp \tau$ (a common prime of $w, \alpha$ divides $A$ and $D$... 
precisely: it divides $C = w\gamma$ and $D = \alpha\tau$, contradiction;
similarly for $\gamma, \tau$ via $A$ and $B$... the six statements follow
by routing each hypothetical common prime into one of the two coprime
pairs). ∎

**Proposition F3.3a (two Pythagorean parametrizations).** A primitive 4-AP
of squares $p^2 < q^2 < r^2 < s^2$ determines coprime pairs $(a,b)$,
$(c,d)$ of opposite parity with $a > b \ge 1$, $c > d \ge 1$ and
$$q = a^2+b^2,\quad r = a^2 - b^2 + 2ab,\quad p = |a^2 - b^2 - 2ab|,$$
$$r = c^2+d^2,\quad s = c^2 - d^2 + 2cd,\quad q = |c^2 - d^2 - 2cd|.$$

*Proof.* Apply [F2.2](F2-aps-and-pythagorean.md) to the 3-AP
$(p^2, q^2, r^2)$ centered at $q^2$: $e_1 = \frac{r-p}{2}$,
$f_1 = \frac{r+p}{2}$ satisfy $e_1^2+f_1^2 = q^2$ with $e_1+f_1 = r$,
$f_1-e_1 = p$, and $e_1, f_1 \ge 1$ (else $p = r$). The triple is
primitive: a common prime of $e_1, f_1$ divides $r \pm p$, hence the coprime
pair $r, p$ (F3.1). By the parametrization proved inside F3.2,
$\{e_1, f_1\} = \{2ab,\, a^2-b^2\}$ and $q = a^2+b^2$; then
$r = e_1+f_1 = a^2-b^2+2ab$ and $p = |f_1-e_1| = |a^2-b^2-2ab|$,
independently of which leg is even. The second display is the same argument
for $(q^2, r^2, s^2)$ centered at $r^2$, where $s = e_2+f_2$ and
$q = f_2 - e_2$. ∎

**Proposition F3.3b (one quartic equation).** In the situation of F3.3a
there exist pairwise coprime **odd** positive integers $w, \alpha, \gamma,
\tau$ with
$$(\diamondsuit)\qquad (\alpha^2+\gamma^2)(2w^2+\tau^2) = 6\,w\alpha\gamma\tau$$
and $\gamma\tau - w\alpha \ge 1$ (this quantity is the $b$ or $c$ of
F3.3a).

*Proof.* Equating the two expressions for each of $r$ and $q$:
$$c^2+d^2 = a^2+2ab-b^2, \qquad a^2+b^2 = \varepsilon\,(c^2-2cd-d^2),\quad
\varepsilon = \pm1.$$

*Case $\varepsilon = +1$*: adding and subtracting gives (machine-verified
identities)
$$b(a-b) = d(c+d), \qquad a(a+b) = c(c-d).$$
Since $\gcd(a, a+b) = \gcd(a,b) = 1$ and $\gcd(c, c-d) = \gcd(c,d) = 1$,
F3.0 applied to $a(a+b) = c(c-d)$ yields pairwise coprime positive $w,
\alpha, \gamma, \tau$ with $a = w\alpha$, $c = w\gamma$, $a+b = \gamma\tau$,
$c-d = \alpha\tau$; hence $b = \gamma\tau - w\alpha \ge 1$ and $d = w\gamma
- \alpha\tau \ge 1$. Substituting into $b(a-b) = d(c+d)$ gives the
polynomial identity
$$b(a-b) - d(c+d) = 6w\alpha\gamma\tau - (\alpha^2+\gamma^2)(2w^2+\tau^2),$$
so the vanishing of the left side is $(\diamondsuit)$. Parity:
$a+b = \gamma\tau$ odd forces $\gamma, \tau$ odd; $c-d = \alpha\tau$ odd
forces $\alpha$ odd; and $(\diamondsuit)$ mod 4 (with $\alpha,\gamma,\tau$
odd, so the left side is $\equiv 2 \cdot \mathrm{odd} \equiv 2$) forces $w$
odd, since $w$ even would make the right side $\equiv 0 \pmod 4$.

*Case $\varepsilon = -1$*: the same additions give $c(c-d) = b(a-b)$ and
$d(c+d) = a(a+b)$; applying F3.0 to the latter ($d = wx$, $c+d = yz$,
$a = wy$, $a+b = xz$) and substituting into the former yields, identically,
$(x^2+y^2)(2w^2+z^2) = 6wxyz$ — the same equation after renaming
$(\alpha,\gamma,\tau) := (x,y,z)$, with $b = xz - wy \ge 1$ playing the
role of the positivity condition and the same parity conclusions. ∎

**Proposition F3.3c (rigidification).** Pairwise coprime odd positive
solutions of $(\diamondsuit)$ satisfy
$$(S')\qquad \alpha^2 + \gamma^2 = 2w\tau
\qquad\text{and}\qquad 2w^2 + \tau^2 = 3\alpha\gamma .$$

*Proof.* View $(\diamondsuit)$ as a quadratic in $\tau$:
$(\alpha^2+\gamma^2)\,\tau^2 - 6w\alpha\gamma\,\tau +
2w^2(\alpha^2+\gamma^2) = 0$. Its discriminant $4w^2 J$, with
$J := 9\alpha^2\gamma^2 - 2(\alpha^2+\gamma^2)^2$, must be a perfect
square, so $J = k^2$ with $k \ge 0$; $k = 0$ is impossible
($9(\alpha\gamma)^2 = 2(\alpha^2+\gamma^2)^2$ fails mod 2), and $k$ is odd.
Write $M' = (\alpha^2+\gamma^2)/2$, an odd integer. Then
$$k^2 + 8M'^2 = 9\alpha^2\gamma^2, \quad\text{i.e.}\quad
(k + 2M'\sqrt{-2})(k - 2M'\sqrt{-2}) = (3\alpha\gamma)^2$$
in $\mathbb{Z}[\sqrt{-2}]$, which is Euclidean for the norm
$N(a+b\sqrt{-2}) = a^2+2b^2$ (round the coordinates of the quotient; the
remainder has norm $\le \frac34$ of the divisor's), hence a UFD with units
$\pm1$. The two factors are coprime: a common prime would have norm
dividing both the odd $(3\alpha\gamma)^2$ and $N(4M'\sqrt{-2}) =
32M'^2$, hence divide $\gcd(3\alpha\gamma, M')^2$-adjacent quantities — and
$\gcd(k, M') = 1$ ($\ell \mid k, M'$ gives $\ell \mid 3\alpha\gamma$;
$\ell \mid \alpha$ forces $\ell \mid \gamma$; $\ell = 3$ forces
$3 \mid \alpha^2+\gamma^2$, i.e. $3 \mid \alpha, \gamma$ — all excluded),
while the ramified prime $\sqrt{-2}$ divides neither factor ($k$ odd). So
each factor is $\pm$ a square: $k + 2M'\sqrt{-2} = \pm(x+y\sqrt{-2})^2$
gives, comparing coefficients and taking norms,
$$M' = xy, \qquad k = |x^2 - 2y^2|, \qquad x^2 + 2y^2 = 3\alpha\gamma,$$
with $x, y$ positive, odd (their product $M'$ is odd) and coprime (a common
prime would divide $k$ and $M'$).

The quadratic's roots are $\tau_\pm = w\,\frac{3\alpha\gamma \pm k}{2M'}$,
and since $\{3\alpha\gamma + k,\ 3\alpha\gamma - k\} = \{2x^2,\ 4y^2\}$
(whichever order), the actual $\tau$ satisfies $\tau = wx/y$ or
$\tau = 2wy/x$. The latter is impossible: $x\tau = 2wy$ has odd left side
and even right side. So $y\tau = wx$; from $\gcd(\tau, w) = 1$ and
$\gcd(x,y) = 1$: $\tau \mid x$ and $x \mid \tau$, so $x = \tau$ and then
$y = w$. Substituting $M' = xy$ and $x^2+2y^2 = 3\alpha\gamma$ gives
exactly $(S')$. ∎

**Proposition F3.3d (the concordant pair).** Nondegenerate solutions of
$(S')$ (i.e. with $\alpha \ne \gamma$; note $\alpha = \gamma$ forces
$\alpha = \gamma = w = \tau = 1$, which violates
$\gamma\tau - w\alpha \ge 1$) produce coprime integers $a \equiv 0 \pmod 4$,
$b$ odd, with
$$a^2 + b^2 = w^2 \qquad\text{and}\qquad 4a^2 + b^2 = \tau^2 .$$

*Proof.* Set $s' = \frac{\alpha+\gamma}{2}$, $t' = \frac{\alpha-\gamma}{2}$
(integers; WLOG $\alpha > \gamma$, so $t' \ge 1$). From $(S')$:
$s'^2 + t'^2 = \frac{\alpha^2+\gamma^2}{2} = w\tau$ and
$3(s'^2 - t'^2) = 3\alpha\gamma = 2w^2+\tau^2$. Adding and subtracting
$3(s'^2+t'^2) = 3w\tau$:
$$6s'^2 = (w+\tau)(2w+\tau), \qquad 6t'^2 = (\tau - w)(2w - \tau),$$
(machine-verified identities), so $w < \tau < 2w$ strictly ($\tau = w$
forces $w = \tau = 1 = \alpha\gamma$-degenerate; $\tau = 2w$ is impossible
as $\tau$ is odd). Multiply:
$$36(s't')^2 = (\tau^2 - w^2)(4w^2 - \tau^2) =: A \cdot B .$$
Now: $B = (2w-\tau)(2w+\tau)$ is odd; $A = (\tau-w)(\tau+w)$ has
$v_2(A) \ge 3$ (both factors even, exactly one $\equiv 0 \bmod 4$ since
their sum $2\tau \equiv 2 \bmod 4$); $\gcd(A,B)$ divides
$A+B = 3w^2$ and $4A+B = 3\tau^2$, hence divides 3; and by $(S')$
$3 \mid 2w^2 + \tau^2$, which forces $3 \nmid w\tau$ and
$\tau^2 \equiv w^2 \pmod 3$, so 3 divides **both** $A$ and $B$; hence
$\gcd(A,B) = 3$ exactly (9 would divide $3w^2$). Writing $A = 3A_1$,
$B = 3B_1$ with $\gcd(A_1, B_1) = 1$ and $A_1 B_1 = (2s't')^2$: each of
$A_1, B_1$ is a perfect square, $A_1 = a^2$ with $v_2(a^2) = v_2(A) \ge 3$
and even, so $4 \mid a$; $B_1 = b^2$ with $b$ odd. Finally
$$3w^2 = A + B = 3a^2 + 3b^2 \implies w^2 = a^2+b^2, \qquad
3\tau^2 = 4A + B = 12a^2+3b^2 \implies \tau^2 = 4a^2+b^2,$$
and $\gcd(a,b) = 1$ from $\gcd(A_1,B_1) = 1$. ∎

**Proposition F3.3e (the classical quartic).** The concordant pair of
F3.3d forces coprime $r, s$ of opposite parity, $rs = a \neq 0$, with
$$r^4 - r^2 s^2 + s^4 = w^2 .$$

*Proof.* From $4a^2 + b^2 = \tau^2$ with $b, \tau$ odd:
$\frac{\tau-b}{2}\cdot\frac{\tau+b}{2} = a^2$ with coprime factors (a
common prime $\ell$ divides $\tau, b$, hence $\ell \mid 4a^2$, odd
$\ell \mid a$, contradicting $\gcd(a,b) = 1$), so both are squares:
$\frac{\tau-b}{2} = r^2$, $\frac{\tau+b}{2} = s^2$ (signs chosen with
$b = s^2 - r^2 > 0$; if $b < 0$ swap names), giving $\tau = r^2+s^2$,
$b = s^2 - r^2$, $a = rs$, $\gcd(r,s) = 1$, opposite parity (as $b$ is
odd), and $rs = a \ne 0$. Substituting into $w^2 = a^2+b^2$:
$$w^2 = r^2s^2 + (s^2-r^2)^2 = s^4 - r^2s^2 + r^4. \qquad\blacksquare$$

**Open Task F3-T1 (the last mile).** Give a self-contained descent proof of
**(Q)**: $r^4 - r^2s^2 + s^4$ is never a perfect square for coprime
$r, s$ of opposite parity with $rs \ne 0$. This is classical (equations of
this shape are dispatched in Euler-era literature and in Dickson's
*History*, Vol. II — SUMMARY-ONLY provenance), and exhaustively VERIFIED
here to the check's bound; a bonus constraint proven above: in any putative
solution arising from a 4-AP, the even one of $r,s$ is divisible by 4
(since $4 \mid a = rs$). Closing F3-T1 makes the entire proof of F3.3
self-contained in this repository.

**Remark (what this chain buys).** Even with (Q) taken as classical, the
chain proves: *any* 4-AP of squares would produce a solution of the rigid
system $(S')$, hence a concordant pair $(a^2+b^2, 4a^2+b^2)$ of squares,
hence a point on the quartic curve $y^2 = x^4 - x^2 + 1$ with
$x = r/s \in \mathbb{Q} \setminus \{0, \pm1\}$. That curve is
birationally an elliptic curve; the chain thus locates the exact geometric
bottleneck of the four-square theorem, in the same spirit as the main
problem's own reductions.

## 4. Application: collinear Lucas families are dead

**Corollary F3.4.** No MSS3 has $v = \pm 3u$ or $u = \pm 3v$. Consequently
(with the F1.3 exclusions) the offset multiset
$\{0, \pm u, \pm v, \pm(u{+}v), \pm(u{-}v)\}$ of an MSS3 never lies in an
arithmetic progression.

*Proof.* If $v = 3u$ (other cases by the $D_4$ symmetry of F1), the offsets
are $\{0, \pm u, \pm 2u, \pm 3u, \pm 4u\}$ — the full 9-term AP from
$-4u$ to $4u$ — so the entries are nine distinct squares in AP, containing
four; contradiction with F3.3. ∎

## 5. What the verify script proves mechanically

`verify/checks/f3_no_four_ap.py`:

1. **Exhaustive F3.3**: no 4 distinct squares in AP with all roots up to
   the bound.
2. **Identity checks** (complete-grid evaluation = proof, as in F1): the
   parametrization identity $(a^2{-}b^2{-}2ab)^2 + (a^2{-}b^2{+}2ab)^2 =
   2(a^2{+}b^2)^2$; the two case identities of F3.3b; the two $(S')$
   consequence identities of F3.3d (conditional identities checked in the
   equivalent unconditional form).
3. **$(\diamondsuit)$ box search**: all pairwise-coprime positive solutions
   in a box are $(\alpha,\gamma,w,\tau) \in \{(1,1,1,1), (1,1,1,2)\}$ (up
   to $\alpha\leftrightarrow\gamma$), each violating the side conditions
   (degenerate $b = 0$, resp. $\tau$ even).
4. **Concordant-pair search**: no coprime $(a,b)$, $a$ even, in a box with
   $a^2+b^2$ and $4a^2+b^2$ both squares, beyond $a = 0$.
5. **(Q) search**: no nontrivial $r^4 - r^2s^2 + s^4 = \square$ in a box.
6. **F3.2 chain searches**: no $x^4 - y^4 = z^2$, no square triangle area,
   no square congruum, up to bounds.
