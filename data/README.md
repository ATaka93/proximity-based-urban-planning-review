# Data

Raw abstract text from Web of Science and Scopus is not redistributed here
due to publisher copyright restrictions.

- Search strings and PRISMA inclusion/exclusion criteria: see
  `/docs/prisma-protocol.md`
- Derived, non-copyrighted data (document-term matrix, tokenized corpus,
  topic-word distributions, co-occurrence edge list, temporal trend tables,
  and manuscript figures) are provided in `/results/` and `/figures/`, not
  in this folder — see those directories and `/scripts/run_pipeline.sh` for
  how each file is generated.
- To reproduce the corpus: rerun the WoS/Scopus queries documented in
  `/docs/prisma-protocol.md` (searched 3 January 2026) and apply the PRISMA
  screening criteria listed there.
- Three DOI lists are provided for transparency, each an independent list
  (not row-aligned to one another — a given row position across files does
  not represent the same paper):
  - `raw-dois-wos.csv` — 1,590 DOIs from the raw Web of Science export
    (pre-deduplication, pre-screening)
  - `raw-dois-scopus.csv` — 2,132 DOIs from the raw Scopus export
    (pre-deduplication, pre-screening)
  - `included-dois.csv` — 968 DOIs for the records that passed abstract
    screening and have a resolvable DOI (968 of 1,027 total included
    records; 59 records in the final corpus lack a DOI in the original
    database export — see `docs/prisma-protocol.md`)

  Anyone with their own database access can use these lists to re-fetch
  abstracts directly, without this repository redistributing the original
  licensed Scopus/WoS export.
