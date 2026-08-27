# A9 — The discrete-sphere model

**Status:** §1 dictionary **PROVEN** (exact identities, machine-checked
by `a9.dictionary`); §2 tension **quantified** (`a9.tension`); §3 the
class-group program **open** (A9-T1). Verification:
`python3 -m verify --only a9`.

## 0. Origin

The owner's geometric picture: the problem is a configuration of
spheres in 9-dimensional space, with solutions the integer points
where they meet, and the all-equal square the point where every
sphere "crosses each number line at the same spot". This document
makes that picture exact and connects it to the classical theory of
**lattice points on spheres** — the "non-solid sphere"
$$\mathcal{S}(n) \;=\; \{(x,y,z) \in \mathbb{Z}^3 :
x^2 + y^2 + z^2 = n\},$$
a finite set with deep arithmetic structure (Gauss: sizes are
class-number-like; Gauss/Venkov: the points are organized by the
class group of $\mathbb{Q}(\sqrt{-n})$ via quaternions; Duke,
after Linnik: the normalized points equidistribute as
$n \to \infty$). *(Classical background, PROVEN-CLASSICAL; used
descriptively — every computed claim below is first-party.)*

## 1. The dictionary (PROVEN, `a9.dictionary`)

Write a magic square of squares in root coordinates, center entry
$m^2$. Every line of a $3\times3$ magic square sums to $3\,\times$
center, so **each of the 8 lines is a point of the single discrete
sphere $\mathcal{S}(3m^2)$**, and the square is 8 such points glued
by shared coordinates (the center root lies on 4 of them, corner
roots on 3, edge roots on 2). Exact facts, verified for every
$m \le 200$ (`compute/discrete_spheres.py`):

- **The trivial point.** $(m, m, m) \in \mathcal{S}(3m^2)$ always —
  the all-equal square: precisely the owner's "same spot on every
  number line" observation.
- **The $m$-slice is A3.** The through-center lines are the sphere
  points with a coordinate equal to $m$, and they biject with the
  congrua set $D(m)$ of
  [A3](A3-simultaneous-congrua.md) via
  $$e^2 + f^2 = m^2,\ d = 2ef \;\longleftrightarrow\;
  (|e-f|,\; m,\; e+f), \qquad
  (e{-}f)^2 + m^2 + (e{+}f)^2 = 3m^2 .$$
  The A3 attack *is* the discrete-circle slice of this sphere: an
  MSS3 with center $m^2$ needs an additive quadruple
  $u, v, u{+}v, u{-}v \in D(m)$, i.e. four slice points in
  arithmetic relation.
- **Parity shadow.** For odd $m$, $3m^2 \equiv 3 \pmod 8$, and every
  three-square representation of a number $\equiv 3 \pmod 8$ has all
  coordinates odd (exhaustive residue check) — the sphere-side
  source of the F4 parity facts.
- **Nodes, and the magic/oblique split.** A subtlety the machine
  check enforces: the square's 8 **magic lines** are the *zero-sum*
  triples of Lucas labels, while the 8 **triple points** of the
  arrangement (where the 256 nodes of $X$ live) are the
  *grid-collinear* triples — and exactly **four** of those are magic
  lines (the $\{a{=}0\}$, $\{b{=}0\}$ and two diagonal pencils,
  i.e. the points $A_0, B_0, D_\pm$: vanishing there collapses a
  whole sphere condition), while the outer four ($A_\pm, B_\pm$) are
  *oblique* triples whose three entries belong to three different
  magic lines. The A8 theorems read: *any 1-parameter family of
  solutions passes through $\ge 3$ of these eight degeneration
  points* — and, pleasingly, the four sphere-collapse points
  $\{A_0, B_0, D_\pm\}$ are exactly the four triple points on the
  central entry line, the set that organizes the special subspaces
  of the A8 §8 classification.

## 2. The tension, quantified (`a9.tension`)

The discrete-sphere view and the surface view pull against each
other, and the table makes it numeric. As $m$ grows the sphere gets
RICH — $|\mathcal{S}(3m^2)|$ reaches 64 already by $m \le 200$, and
grows on average like a class number (Duke: the points spread
uniformly) — so naive counting heuristics predict compatible
configurations should appear. Yet the compatibility ladder on the
slice stays EMPTY: for all $m \le 200$ (and A3's far larger desert
bounds), the additive-triple and additive-quadruple counts are
$$L_3 = L_4 = 0$$
— abundance without compatibility. The surface side explains the
scarcity structurally ($X$ is of general type, quasi-hyperbolic,
with every curve forced through the sphere-degeneration points); the
Bombieri–Lang philosophy predicts at most finitely many
nondegenerate points, against the heuristic's optimism. Any
resolution of the problem must reconcile exactly these two forces.

## 3. The class-group program (open)

- **A9-T1 (the torsor formulation).** Via Gauss/Venkov, the points
  of $\mathcal{S}(n)$ carry the action of the class group of
  $\mathbb{Q}(\sqrt{-n})$. Formulate the 8-point glued configuration
  as a system of relations in that torsor; derive genus-theory
  constraints on configurations (the computable first layer — it
  should recover, and may strengthen, the F4 congruences), then ask
  what the full class-group structure forbids. The $m$-slice case is
  the Gaussian-integer layer already exploited by A3.
- **A9-T2 (acquisitions, backlog).** Duke (Invent. Math. 92, 1988)
  and Aka–Einsiedler–Shapira (joint equidistribution of lattice
  points and orthogonal lattices) — background for any density-style
  argument; added to [papers/WANTED.md](../../papers/WANTED.md)
  backlog.

## 4. What the verify script proves mechanically

`verify/checks/a9_spheres.py`: the all-lines-on-one-sphere identity
(symbolic, via the Lucas parametrization), the trivial point, the
exact slice $\leftrightarrow$ $D(m)$ bijection for every $m$ up to
the profile bound, the all-odd residue fact, and the pinned tension
table (max sphere size vs $L_3 = L_4 = 0$).
