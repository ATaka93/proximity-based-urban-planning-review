# Conceptual Evolution of Proximity-Based Urban Planning

Reproducible NLP pipeline (LDA topic modelling + co-occurrence network analysis)
mapping the conceptual evolution of the X-minute city / proximity-based urban
planning literature, 1992–2026.

**Author:** Aikaterini Taka, PhD Student, Department of Geography, University of the Aegean

**Supervisor:** Assoc. Prof. Dimitris Kavroudakis, Department of Geography, University of the Aegean

**Contact:** ktaka@aegean.gr

> **Note (temporary):** An anonymized version of this repository for double-anonymized
> peer review is available at [link — add once generated via anonymous.4open.science].
> This full repository is the canonical public version and will remain the reference
> copy going forward.

## Status

This repository accompanies a manuscript currently under submission.
Citation details and a Zenodo DOI will be added upon publication.

## Summary

A PRISMA-guided systematic review of 1,027 peer-reviewed publications (screened
from 2,366) on proximity-based urban planning, analyzed using LDA topic modelling
(k=6) and a PMI-weighted co-occurrence network with Louvain community detection,
validated via statistical significance testing.

## Research questions

- **RQ1 — Articulation & Definitions:** How have X-minute city and proximity-based
  urban concepts been defined and articulated across academic publications?
- **RQ2 — Clustering:** What thematic clusters emerge from the corpus and which
  terms co-occur most frequently within them?
- **RQ3 — Evolution:** How have the dominant thematic groupings and research
  emphases shifted over publication years?

**Note on RQ3:** the current repository scripts (`preprocess.py`,
`model_selection.py`, `lda_model.py`, `cooccurrence_network.py`,
`network_significance.py`) produce the topic model and co-occurrence network
(RQ1–RQ2) but do not yet include a temporal-trend analysis script. Any
year-over-year findings reported in the manuscript should be treated as
pending reproducibility until such a script is added here — see
"Key findings" below.

## Repository structure
├── data/ # derived, non-copyrighted data (see data/README.md)
├── scripts/ # preprocessing, model selection, LDA, network analysis, and significance testing
├── results/ # topic outputs, network statistics, model-selection diagnostics
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
   python3 scripts/model_selection.py --dtm results/dtm.npz --tokenized results/tokenized_corpus.csv --outdir results
   python3 scripts/lda_model.py --dtm results/dtm.npz --vocab results/vocabulary.csv --outdir results
   python3 scripts/cooccurrence_network.py --input results/tokenized_corpus.csv --outdir results
   python3 scripts/network_significance.py --edges results/cooccurrence_edges_pmi.csv --outdir results
```

Step 2 (`model_selection.py`) statistically evaluates candidate values of k
via held-out perplexity and topic coherence; step 5 (`network_significance.py`)
tests whether the co-occurrence network's modularity is statistically
significant against a degree-preserving random null model. Neither step is
strictly required to reproduce the topic/network outputs themselves, but
both are what justify the parameter choices used in the manuscript (see
`docs/topic-codebook.md`).

All parameters (CountVectorizer max_df/min_df, LDA k/max_iter, co-occurrence
network's min document frequency/min co-occurrence count) default to the
values reported in `docs/prisma-protocol.md` and `docs/topic-codebook.md`,
and can be overridden via command-line flags — run any script with `--help`
to see options.

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
- **Temporal and keyword-frequency trends** (topic dominance over time,
  keyword frequency growth) reported in the manuscript are not yet
  reproduced by a script in this repository — see the RQ3 note above

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
edge list) are provided in `results/`.

## License

Code is released under the MIT License (see `LICENSE`). Text and figures are
released under CC-BY-4.0 unless otherwise noted.
