# Conceptual Evolution of Proximity-Based Urban Planning

Reproducible NLP pipeline (LDA topic modelling + co-occurrence network analysis)
mapping the conceptual evolution of the X-minute city / proximity-based urban
planning literature, 1992–2026.

**Author:** Aikaterini Taka, PhD Student, Department of Geography, University of the Aegean

**Supervisor:** Assoc. Prof. Dimitris Kavroudakis, Department of Geography, University of the Aegean

**Contact:** ktaka@aegean.gr

Presented at City+2026: 9th International Conference on Interdisciplinary Urban
Studies, July 3, 2026.

> **Note (temporary):** An anonymized version of this repository for double-anonymized
> peer review is available at [link — add once generated via anonymous.4open.science].
> This full repository is the canonical public version and will remain the reference
> copy going forward.

## Status

This repository accompanies a manuscript currently under submission.
Citation details and a Zenodo DOI will be added upon publication.

## Summary

A PRISMA-guided systematic review of 1,040 peer-reviewed publications (screened
from 2,366) on proximity-based urban planning, analyzed using LDA topic modelling
(k=6) and Louvain co-occurrence network community detection. The analysis
identifies a quantifiable paradigm shift from the compact city framework (T2,
71% dominance in 2018) to the 15-minute city / proximity planning framework
(T5, 81% dominance by early 2026), with "accessibility" as a central bridging
concept and "equity" as a fast-emerging research dimension since 2022.

## Research questions

- **RQ1 — Articulation & Definitions:** How have X-minute city and proximity-based
  urban concepts been defined and articulated across academic publications?
  
- **RQ2 — Clustering:** What thematic clusters emerge from the corpus and which
  terms co-occur most frequently within them?
  
- **RQ3 — Evolution:** How have the dominant thematic groupings and research
  emphases shifted over publication years?

## Repository structure

├── data/ # derived, non-copyrighted data (see data/README.md)

├── scripts/ # preprocessing, LDA, and network analysis code

├── results/ # topic outputs, network statistics, figures

├── docs/ # PRISMA flow diagram, protocol, topic codebook

├── LICENSE # MIT (code)

├── CITATION.cff

└── README.md

## Methodology

1. **Corpus compilation** — Web of Science + Scopus, 2,366 records screened
2. **PRISMA filtering** — 1,040 abstracts included
3. **Text pre-processing** — tokenisation, lemmatisation
4. **LDA topic modelling** — Document-term matrix built with CountVectorizer
   (max_df=0.90, min_df=5); LDA via scikit-learn, k=6 topics, 30 iterations
5. **Co-occurrence network** — Louvain community detection, edge threshold n ≥ 20

## Reproducing the pipeline

Requires Python 3.12 (tested; earlier 3.x likely works but is unverified).

1. Install dependencies:
```bash
   pip install -r requirements.txt
```
2. On first run, NLTK will automatically download required tokenizer/stopword/
   lemmatizer data (`punkt`, `stopwords`, `wordnet`) — this requires an
   internet connection the first time only.
3. Place the corpus at `data/abstracts.csv` with at minimum an `abstract`
   column (see `data/README.md` for how to reconstruct this from the PRISMA
   protocol, since raw WoS/Scopus text cannot be redistributed).
4. Run the full pipeline:
```bash
   bash scripts/run_pipeline.sh
```
   Or run each step individually:
```bash
   python3 scripts/preprocess.py --input data/abstracts.csv --outdir results
   python3 scripts/lda_model.py --outdir results
   python3 scripts/cooccurrence_network.py --outdir results
```

All parameters (CountVectorizer max_df/min_df, LDA k/max_iter, co-occurrence
threshold) default to the values reported in `docs/prisma-protocol.md` and
the manuscript, and can be overridden via command-line flags — run any
script with `--help` to see options.

## Key findings

- **Six latent topics** identified: (T1) Walkability & Built Environment,
  (T2) Compact City & Sustainable Form, (T3) Transit-Oriented Development,
  (T4) Housing & Land Markets, (T5) 15-Min City & Proximity Planning,
  (T6) Health, Wellbeing & Urban Environment
- **Three co-occurrence communities:** Proximity & Access (32 nodes),
  Compact Form & Land (30 nodes), Transport & Travel (7 nodes) —
  69 nodes, 1,892 edges, Louvain modularity Q = 0.059
- **Temporal shift:** T2 dominated in 2018 (71%); T5 overtook T2 by 2021;
  T5 exceeded 70% share by 2023; T5 reached ~81% by early 2026
- **Keyword trends:** "minute" grew fastest (0 → 20.8 per 1,000 words);
  "accessibility" reached 12.7 per 1,000 words by 2026; "proximity" nearly
  tripled 2022–2026; "equity" emerged as a new dimension post-2022

## Software

- Python [add version]
- scikit-learn [add version]
- [add: networkx / python-louvain / spaCy / NLTK — whichever you used, with versions]

## Data availability

Raw WoS/Scopus abstracts are not redistributed here due to publisher copyright
restrictions. See `data/README.md` for search strings, PRISMA criteria, and
instructions for reproducing the corpus. Derived, non-copyrighted data
(tokenized corpus, document-term matrix, topic-word distributions, co-occurrence
edge list) are provided in `data/`.

## License

Code is released under the MIT License (see `LICENSE`). Text and figures are
released under CC-BY-4.0 unless otherwise noted.
