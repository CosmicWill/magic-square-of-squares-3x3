# Research log

Dated, append-only. Negative results and failed attempts are logged with the
same care as positive ones — an autopsy per failure. Newest entries at the
bottom.

---

## 2026-08-25 — Entry 0: project start, environment probe

**Decisions made at kickoff** (user-confirmed): goal = impossibility proof
attempts (partial results accepted as the realistic outcome); write-ups in
Markdown; no Lean — rigor = complete classical proofs + mechanical
verification (`python3 -m verify`).

**Environment probe results:**

| Tool | Result |
|---|---|
| Python | 3.11.15 (stdlib `math.isqrt`, native bigints) |
| sympy | 1.14.0 — installed OK via pip |
| gmpy2 | 2.3.1 — installed OK via pip |
| PARI/GP | **2.15.4 installed OK via apt** (has `ellrank`) — elliptic-curve rank experiments unblocked |
| gcc / Rust | 13.3.0 / 1.94.1 available (fast-search stretch goals) |
| LaTeX / Lean | absent by design (Markdown-only; no formalization this phase) |
| Network | PyPI + apt reachable through proxy; **general WebFetch blocked** (arXiv/Wikipedia/multimagie unfetchable) — literature is therefore SUMMARY-ONLY unless stated otherwise, see `docs/references.md` |

**Rule adopted:** proof-critical verification runs on pure stdlib; sympy /
gmpy2 / PARI are allowed only in exploratory scripts and in checks that SKIP
cleanly when absent. Rank *upper* bounds without PARI would be CITED/SKIPPED,
never silently degraded — with PARI present we can do better.

**Plan of record:** foundations F1–F6 proven from scratch with named checks;
attack lines in order — A1 (audit of the unrefuted arXiv:2510.08286 claimed
proof), A2 (function field $\mathbb{F}_q(t)$ analogue — apparently virgin
territory, Mason–Stothers available), A3 (simultaneous congrua & the
$\mathbb{Q}$ vs $\mathbb{Q}(i,\sqrt{n})$ descent gap), A4 (the open
eight-square case), A5/A6 (surface geometry & search bounds as precise
stubs + small verified nuggets).
