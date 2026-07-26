# Conceptual Evolution of Proximity-Based Urban Planning

Reproducible NLP pipeline (LDA topic modelling + co-occurrence network analysis)
mapping the conceptual evolution of the X-minute city / proximity-based urban
planning literature, 1992–2026.

**Author information withheld for double-anonymized peer review.**

> **Note (temporary):** This is an anonymized version of the repository for
> double-anonymized peer review. The full, attributed version will be available upon acceptance.

## Status

This repository accompanies a manuscript currently under submission.
Citation details and a Zenodo DOI will be added upon publication.

## Summary

A PRISMA-guided systematic review of 1,027 peer-reviewed publications (screened
from 2,366) on proximity-based urban planning, analyzed using LDA topic modelling
(k=6), a PMI-weighted co-occurrence network with Louvain community detection
validated via statistical significance testing, and a temporal trend analysis
of topic share and keyword frequency by publication year.

## Research questions

- **RQ1 — Articulation & Definitions:** How have X-minute city and proximity-based
  urban concepts been defined and articulated across academic publications?
- **RQ2 — Clustering:** What thematic clusters emerge from the corpus and which
  terms co-occur most frequently within them?
- **RQ3 — Evolution:** How have the dominant thematic groupings and research
  emphases shifted over publication years?

RQ1–RQ2 are addressed by the topic model and co-occurrence network
(`lda_model.py`, `cooccurrence_network.py`). RQ3 is addressed by
`temporal_analysis.py`, which computes topic dominance share and keyword
frequency by year (see "Key findings" below).

## Repository structure
├── data/ # derived, non-copyrighted data (see data/README.md)
├── scripts/ # preprocessing, model selection, LDA, network analysis, significance testing, temporal trends
├── results/ # topic outputs, network statistics, model-selection diagnostics, temporal trend data
├── docs/ # PRISMA flow diagram, protocol, topic codebook
├── LICENSE # MIT (code)
└── README.md

## Methodology

1. **Corpus compilation** — Web of Science + Scopus, 2,366 records screened
   (searched 3 January 2026)
2. **PRISMA filtering** — 1,027 abstracts included (see `docs/prisma-protocol.md`)
3. **Text pre-processing** — copyright-boilerplate stripping, tokenisation,
   lemmatisation, stopword removal (domain, geographic, and academic-
   boilerplate lists; see `scripts/preprocess.py`)
4. **LDA topic modelling** — Document-term matrix built with CountVectorizer
   (max_df=0.90, min_df=5); LDA via scikit-learn, k=6 topics, 30 iterations.
   k=6 evaluated against held-out perplexity and topic coherence (c_v) — see
   `docs/topic-codebook.md` for the full disclosed trade-off
5. **Co-occurrence network** — PMI-weighted edges (positive PMI, minimum
   co-occurrence count of 5) over all terms with document frequency ≥ 20;
   Louvain community detection; modularity significance tested against 20
   degree-preserving random-network permutations
6. **Temporal trend analysis** — topic dominance share and keyword
   frequency (per 1,000 words) computed by publication year, addressing RQ3

## Reproducing the pipeline

Requires Python 3.12 (tested; earlier 3.x likely works but is unverified).

1. Install dependencies:
```bash
   pip install -r requirements.txt
```
2. On first run, NLTK will automatically download required tokenizer/stopword/
   lemmatizer data (`punkt`, `stopwords`, `wordnet`) — this requires an
   internet connection the first time only.
3. Place the corpus at `data/abstracts.csv` with at minimum `abstract` and
   `year` columns (see `data/README.md` for how to reconstruct this from
   the PRISMA protocol, since raw WoS/Scopus text cannot be redistributed).
4. Run the full pipeline:
```bash
   bash scripts/run_pipeline.sh
```
   Or run each step individually:
```bash
   python3 scripts/preprocess.py --input data/abstracts.csv --outdir results
   python3 scripts/model_selection.py --dtm results/dtm.npz --tokenized results/tokenized_corpus.csv --outdir results
   python3 scripts/lda_model.py --dtm results/dtm.npz --vocab results/vocabulary.csv --outdir results
   python3 scripts/cooccurrence_network.py --input results/tokenized_corpus.csv --outdir results
   python3 scripts/network_significance.py --edges results/cooccurrence_edges_pmi.csv --outdir results
   python3 scripts/temporal_analysis.py --tokenized results/tokenized_corpus.csv --doc-topic results/lda_doc_topic.csv --outdir results
```

Steps 2 and 5 (`model_selection.py`, `network_significance.py`) statistically
justify the k=6 and network-community choices respectively; step 6
(`temporal_analysis.py`) is what directly answers RQ3. None of these three
are required to reproduce the core topic/network outputs, but all three are
what make the manuscript's specific numerical claims reproducible from this
repository rather than only asserted.

All parameters (CountVectorizer max_df/min_df, LDA k/max_iter, co-occurrence
network's min document frequency/min co-occurrence count, temporal-analysis
keyword list) default to the values reported in `docs/prisma-protocol.md`
and `docs/topic-codebook.md`, and can be overridden via command-line flags —
run any script with `--help` to see options.

## Key findings

- **Six latent topics** identified (k=6, statistically evaluated — see
  `docs/topic-codebook.md`): (T1) X-Minute City & Accessibility,
  (T2) Compact City Policy & Residential Form, (T3) Urban Form, Density &
  Emissions, (T4) Sustainable Design & Policy Strategy, (T5) Housing, Green
  Space & Landscape, (T6) Walkability & Health
- **Four co-occurrence communities**, validated via PMI-weighted network
  construction: X-Minute City, Proximity & Accessibility (n=246);
  Neighbourhood & Residential Density (n=268); Walkability, Active Travel &
  Health (n=131); Sustainability & Policy Strategy (n=310) — 955 nodes,
  75,330 edges, 16.5% density, modularity Q = 0.1764, statistically
  significant against a degree-preserving random null model
  (Z = 28.99, p < 0.0001; see `results/network_significance.txt`)
- **Substantive finding on topic separation:** pollution/emission/air-quality
  terms load onto the urban-form/density topic (T3), not the
  walkability/health topic (T6) — these are two separate literatures in this
  corpus, not one combined "environment and health" theme
- **Temporal shift** (see `results/topic_share_by_year.csv`): T2 (Compact
  City Policy) dominated the literature through the 1990s–2000s (33–71%
  share in years with meaningful sample sizes). T1 (X-Minute City &
  Accessibility) was negligible before 2018 and grew to 35.5% by 2023,
  46.5% by 2024, and 51.3% by 2025 — a genuine and substantial shift toward
  X-minute-city framing, though less sharply defined than a single dominant
  topic overtaking another, since T4 (Sustainable Design & Policy Strategy)
  remained co-dominant throughout the same period (24–44% share, 2020–2025).
  Early-year shares (pre-2010, n=1–18 documents/year) should be treated with
  caution given small sample sizes; 2026 (n=21) is a partial-year
  observation (see search-date note in `docs/prisma-protocol.md`).
- **Keyword trends** (see `results/keyword_frequency_by_year.csv`):
  "accessibility" shows a clear growth trend, from ~2.3 per 1,000 words in
  2018 to 13.8 per 1,000 words in 2026. "Proximity" similarly grew, from
  ~1.0 to 7.1 per 1,000 words over the same period. "Equity" is present only
  sparsely and inconsistently across years (mostly below 2 per 1,000 words
  even in recent years) — its emergence as a research dimension is weaker
  and noisier in this corpus than a clean "post-2022 emergence" narrative
  would suggest, and should be reported with that caveat. "Minute" and
  "walkability" frequencies are volatile year-to-year without a clean
  monotonic trend, likely due to topic-specific vocabulary (e.g. "15-minute")
  being partly absorbed into hyphenation/lemmatization during preprocessing.

## Software

- Python 3.12
- scikit-learn 1.8.0
- nltk 3.10.0
- networkx 3.6.1
- python-louvain 0.16
- pandas 3.0.2
- scipy 1.17.1
- joblib 1.5.3
- gensim 4.4.0
- numpy 2.4.4

Exact pinned versions are in `requirements.txt` — install with
`pip install -r requirements.txt` for a reproducible environment.

## Data availability

Raw WoS/Scopus abstracts are not redistributed here due to publisher copyright
restrictions. See `data/README.md` for search strings, PRISMA criteria, and
instructions for reproducing the corpus. Derived, non-copyrighted data
(tokenized corpus, document-term matrix, topic-word distributions, co-occurrence
edge list, temporal trend tables) are provided in `results/`.

## License

Code is released under the MIT License (see `LICENSE`). Text and figures are
released under CC-BY-4.0 unless otherwise noted.
