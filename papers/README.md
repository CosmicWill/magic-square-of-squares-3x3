# papers/ — acquired primary sources

This working environment cannot fetch most of the web (the egress proxy
allows only PyPI, apt, and GitHub git traffic; arXiv, publisher sites and
personal pages are blocked — attempts are logged in RESEARCH_LOG.md). The
project's literature knowledge is therefore SUMMARY-ONLY (search-snippet
provenance) unless a primary source lands in this directory.

**Workflow:**

1. [WANTED.md](WANTED.md) lists the sources we need, in priority order,
   with exact IDs and links.
2. Drop the PDFs (and any ancillary tarballs/code) into this directory,
   named like `1912.08908v3.pdf`, `1912.08908-anc.tar.gz`,
   `stoll-testa-1009.0388.pdf` — any reasonable name works; keep the
   arXiv ID or author-year visible.
3. Commit/push (or just tell Claude they're here). Each source is then
   read and digested: its provenance flag in `docs/references.md` is
   upgraded from SUMMARY-ONLY to **READ**, claims that were quarantined
   as unverified get resolved, and follow-on work that was blocked on it
   gets scheduled.

Copyright note: only upload what you may lawfully store in this
repository (arXiv PDFs and open-access journal PDFs are fine; if the
repo is public, prefer arXiv versions over paywalled publisher PDFs).

**Acquired so far:**

| Source | Directory | Status |
|---|---|---|
| BTVA, arXiv:1912.08908v3 (source + ancillary Magma) | [1912.08908/](1912.08908/) | READ & digested 2026-08-26 (A7 §7; `verify --only a7btva`) |
| García-Fritz–Urzúa, arXiv:1804.07671 | `1804.07671-garcia-fritz-urzua.pdf` | READ in full 2026-08-26 (A8 method source) |
| Stoll–Testa, arXiv:1009.0388v2 (2025 update) | `1009.0388-stoll-testa.pdf` | READ (main theorems) 2026-08-26 |
| Horie–Yamauchi, arXiv:2512.22520v3 | `2512.22520-horie-yamauchi.pdf` | READ (main theorem) 2026-08-26 |
| Lu–Miyaoka, MRL 2 (1995) | `lu-miyaoka-1995-mrl2.pdf` | READ (main theorems; hypotheses fail for X) 2026-08-26 |
| Miyaoka, Publ. RIMS 44 (2008) | `miyaoka-2008-orbibundle-rims44.pdf` | READ (main theorems; hypotheses fail for X) 2026-08-26 |
| Bruin–Ilten–Xu, arXiv:2312.01722 | `2312.01722-bruin-ilten-xu.pdf` | READ (framework) 2026-08-26 |
