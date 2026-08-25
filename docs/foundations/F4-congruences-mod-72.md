# F4 — Congruence conditions: entries ≡ 1 (mod 24), magic sum ≡ 3 (mod 72)

**Status: PROVEN** (F4.1 with a machine enumeration of its finite core;
F4.2 with a complete proof whose classical quadratic-residue inputs are
proved via Gauss's lemma and verified computationally).
Verification: `python3 -m verify --only f4`.

These are the sharpest *purely congruence* facts about the problem —
[F5](F5-local-solubility.md) proves congruences can go no further than
pruning. Statements are for **primitive** squares
([Definition 0.6](../00-problem-statement.md)); the general case follows by
scaling (Prop. 0.5). First obtained by Pierrat–Thiriet–Zimmermann (2015,
SUMMARY-ONLY provenance); reproved here from scratch.

## Theorem F4.1

Let $L(c,u,v)$ be a primitive MSS3. Then $24 \mid u$, $24 \mid v$, every
entry is $\equiv 1 \pmod{24}$, and the magic sum satisfies
$S \equiv 3 \pmod{72}$.

*Proof.* Squares are $\equiv 0, 1 \pmod 4$.

**Mod 4.** If $c \equiv 0 \pmod 4$: from $c \pm u \in \{0,1\}$, both $u$
and $-u$ lie in $\{0,1\} \bmod 4$, forcing $u \equiv 0$; likewise
$v \equiv 0 \pmod 4$. Then all nine entries are $\equiv 0 \pmod 4$, so all
nine roots are even — contradicting primitivity. If $c \equiv 1 \pmod 4$:
$1 \pm u \in \{0,1\} \bmod 4$ forces $u \equiv 0 \pmod 4$ (check $u \equiv
1, 2, 3$ each put one of $1 \pm u$ outside $\{0,1\}$); likewise $v$. The
remaining possibilities $c \equiv 2, 3$ are not squares. Hence
$c \equiv 1 \pmod 4$, $u \equiv v \equiv 0 \pmod 4$, and **all entries are
odd**.

**Mod 8.** Odd squares are $\equiv 1 \pmod 8$. From $c + u \equiv 1$ and
$c \equiv 1$: $8 \mid u$; likewise $8 \mid v$.

**Mod 3.** Squares are $\equiv 0, 1 \pmod 3$. If $c \equiv 0$: as in the
mod-4 step, $u \equiv v \equiv 0 \pmod 3$, all entries $\equiv 0 \pmod 3$,
all roots divisible by 3 — contradicting primitivity. So $c \equiv 1
\pmod 3$, and $1 \pm u \in \{0,1\} \bmod 3$ forces $u \equiv 0 \pmod 3$;
likewise $v$.

Combining: $24 \mid u, v$, so every entry $\equiv c \pmod{24}$, and $c$ is
$\equiv 1 \pmod 8$ and $\pmod 3$, i.e. $c \equiv 1 \pmod{24}$. Finally
$S = 3c \equiv 3 \pmod{72}$. ∎

**Corollary.** The center root $m$ ($c = m^2$) is odd and $3 \nmid m$; all
nine roots are odd and coprime to 3. Moreover the four offsets, being
congrua of the odd $m$ ([F2.5](F2-aps-and-pythagorean.md)), are
automatically $\equiv 0 \pmod{24}$: for any decomposition $m^2 = e^2+f^2$
with $m$ odd, the even leg is divisible by 4 (its primitive part is
$2ab$ with $ab$ even) so $8 \mid 2ef$; and $3 \mid ef$ whether or not
$3 \mid m$ (if $3 \nmid m$, exactly one of $e^2, f^2$ is $\equiv 0
\bmod 3$; if $3 \mid m$, both are). The two routes to "offsets
$\equiv 0 \pmod{24}$" agree — a consistency check the script performs.

## The machine core (`f4.mod72`)

The proof above is a finite case analysis, so we also **enumerate it
completely**: over all $(c, u, v) \in (\mathbb{Z}/72)^3$ such that

1. all nine Lucas entries are squares mod 72 (i.e. lie in
   $\{x^2 \bmod 72\}$), and
2. not all entries are $\equiv 0 \pmod 4$, and not all are $\equiv 0
   \pmod 9$ (the mod-72 shadow of primitivity: all roots even, resp. all
   divisible by 3, is excluded),

**every** surviving triple has all entries $\equiv 1 \pmod{24}$ and
$3c \equiv 3 \pmod{72}$. Since any primitive integer MSS3 reduces mod 72
to such a triple, this enumeration is a complete, independent proof of
F4.1. (Both proofs are kept: the prose explains *why*, the enumeration
removes case-analysis risk.)

## Theorem F4.2 (prime constraints on the entries)

Let $L(m^2, u, v)$ be a primitive MSS3 and $\ell$ an odd prime with
$\ell \equiv 3$ or $5 \pmod 8$.

1. If $\ell$ divides **any** off-center entry, then $\ell \mid m$.
2. If $\ell \equiv 5 \pmod 8$, then $\ell$ divides **no middle-side
   entry** (the four entries $m^2 \pm (u{+}v)$, $m^2 \pm (u{-}v)$) at all.

*Proof.* (1) Every off-center entry $p^2$ has an opposite entry $q^2$
through the center with $p^2 + q^2 = 2m^2$ (F1). Suppose $\ell \mid p$ and
$\ell \nmid m$. Then $q^2 \equiv 2m^2 \pmod \ell$; also $\ell \nmid q$
(else $\ell^2 \mid p^2 + q^2 = 2m^2$ gives $\ell \mid m$). Hence
$(q\,m^{-1})^2 \equiv 2$: **2 is a quadratic residue mod $\ell$**, so
$\ell \equiv \pm 1 \pmod 8$ (proved below) — contradiction.

(2) Let $\ell \equiv 5 \pmod 8$ divide the middle-side entry
$m^2 - (u{+}v) = p^2$; by (1), $\ell \mid m$, so $\ell^2 \mid m^2$ and
$\ell^2 \mid p^2$ gives $u + v \equiv 0 \pmod{\ell^2}$... precisely:
$\ell \mid p$ and $\ell \mid m$ force $\ell \mid q$ (from $q^2 = 2m^2 -
p^2$), and then $\ell^2$ divides $m^2 \pm (u{+}v)$, so $\ell^2 \mid u+v$.
Now consider the corners $g^2 = m^2 + u$ and $h^2 = m^2 + v$: modulo
$\ell$, $g^2 \equiv u$ and $h^2 \equiv v \equiv -u$. If $\ell \mid u$,
then $\ell \mid v$, and *every* entry is divisible by $\ell$ — hence every
root, contradicting primitivity. So $u \not\equiv 0$, and $u \equiv g^2$
is a nonzero quadratic residue mod $\ell$. Next, the middle-row entry
$r^2 = m^2 - (u{-}v) \equiv -(u - v) \equiv -2u \pmod \ell$ (using $v
\equiv -u$). If $\ell \mid r$: with $\ell \mid$ its opposite $s$ (same
argument as before via $r^2+s^2 = 2m^2$), we get $\ell^2 \mid u - v$,
hence $\ell \mid 2u$, $\ell \mid u$ — just excluded. So $r \not\equiv 0$
and $-2u \equiv r^2$ is a nonzero QR. Then
$-2 \equiv r^2 (g^2)^{-1} \cdot$(unit square) is a QR mod $\ell$. But for
$\ell \equiv 5 \pmod 8$, $-1$ is a QR and $2$ is not, so $-2$ is **not** a
QR — contradiction. ∎

**Quadratic residue inputs (PROVEN-CLASSICAL, proofs included).**
$-1$ is a QR mod odd $\ell$ iff $\ell \equiv 1 \pmod 4$ (proved in
[F2.6b](F2-aps-and-pythagorean.md)). For 2: by **Gauss's lemma**
($\chi(a) = (-1)^\mu$, $\mu = \#\{1 \le k \le \frac{\ell-1}{2} :
ak \bmod \ell > \ell/2\}$ — proof: multiply the congruences
$ak \equiv \pm r_k$ with distinct $r_k \in (0, \ell/2)$; the $r_k$ are a
permutation of $1..\frac{\ell-1}{2}$ since $r_j = r_k$ forces
$a(j \pm k) \equiv 0$, impossible for $0 < j \pm k \cdots < \ell$;
multiplying all gives $a^{(\ell-1)/2} \equiv (-1)^\mu$, and Euler's
criterion identifies the left side with $\chi(a)$), applied to $a = 2$:
$\mu = \frac{\ell-1}{2} - \lfloor \ell/4 \rfloor$, which is even iff
$\ell \equiv \pm 1 \pmod 8$ (four-case check). Hence also: $-2$ is a QR
iff $\ell \equiv 1, 3 \pmod 8$. The script verifies all three criteria
against Euler's criterion for every odd prime up to a bound.

**Scope note.** F4.2's proof also shows: for $\ell \equiv 3 \pmod 8$ the
"deep case" ($\ell \mid m$) survives — $-2$ *is* a QR there — so
middle-side entries divisible by $\ell \equiv 3 \pmod 8$ are not excluded,
only forced to come with $\ell \mid m$. The gauntlet-relevant content:
these constraints are *pruning* facts, consistent with AB1 and all F5
witnesses (checked mechanically).

## What the verify script proves mechanically

`verify/checks/f4_congruences.py`:

1. `f4.mod72` — the complete enumeration described above (373,248 triples).
2. `f4.ap_prime_lemma` — the AP-level core of F4.2(1) against data: for
   every 3-AP of squares $(p^2, m^2, q^2)$ with $m \le$ bound, every prime
   $\ell \equiv 3, 5 \pmod 8$ dividing $pq$ divides $m$.
3. `f4.qr_criteria` — the three QR criteria against Euler's criterion for
   all odd primes $\le$ bound.
4. `f4.offsets_24` — congrua of odd $m$ are $\equiv 0 \pmod{24}$
   (consistency of the Corollary), for all $m \le$ bound.
5. `f4.ab1_consistency` — all nine of AB1's entries (squares and
   non-squares alike) are $\equiv 1 \pmod{24}$, its four offsets are
   $\equiv 0 \pmod{24}$, and its magic sum is $\equiv 3 \pmod{72}$: the
   nearest known object to an MSS3 sits squarely inside the F4.1 residue
   class, a consistency check on the theorem (and a hint that the
   congruence layer genuinely cannot separate AB1-like near-misses from
   putative solutions).
