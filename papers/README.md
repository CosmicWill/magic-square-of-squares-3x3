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
