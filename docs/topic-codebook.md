# Topic Codebook

Interpretive labels assigned to the six latent topics (T1–T6) identified via
LDA (k=6) on the cleaned corpus of 1,027 abstracts (see `docs/prisma-protocol.md`
for corpus construction and `scripts/preprocess.py` for cleaning steps,
including removal of publisher copyright boilerplate, geographic names, and
generic academic-writing terms).

## Choice of k: a disclosed trade-off, not an automatic result

Two standard metrics were used to evaluate candidate values of k (see
`scripts/model_selection.py`, output in `results/model_selection_perplexity.csv`
and `results/model_selection_coherence.csv`):

| k | Held-out perplexity | Topic coherence (c_v) |
|---|---|---|
| **3** | **2139.23 (best)** | **0.3845 (best)** |
| 4 | 2450.28 | 0.3800 |
| 5 | 2731.58 | 0.3813 |
| **6** | 3002.05 | 0.3633 |
| 7 | 3323.97 | 0.3743 |
| 8 | 3694.72 | 0.3773 |
| 9 | 4095.20 | 0.3742 |
| 10 | 4391.77 | 0.3729 |

Both metrics favour k=3 over k=6 on this cleaned corpus. This is disclosed
plainly rather than omitted: **k=6 is not the statistically optimal value**
by either held-out perplexity or topic coherence.

k=6 was nonetheless retained, for two reasons:

1. The coherence gap between k=3 (0.3845) and k=6 (0.3633) is modest
   (≈5.7% relative difference), not a case where k=6 is a poor fit — just
   not the technical optimum.
2. A k=3 solution collapses the corpus into three very broad topics
   (X-Minute City/Accessibility; Housing/Density; Compact Policy/
   Sustainability) that cannot distinguish walkability/health, transport,
   or green-space research from one another. The study's research
   questions (RQ1–RQ3) require tracking a conceptual shift across
   identifiable sub-themes over time, which a 3-topic solution cannot
   support regardless of its coherence score.

This follows guidance from Chang et al. (2009, "Reading Tea Leaves: How
Humans Interpret Topic Models") that automated coherence/perplexity metrics
should inform, not dictate, topic-count selection — held-out likelihood in
particular is documented to correlate poorly with human judgments of topic
quality. The trade-off is stated here explicitly so it can be assessed by
reviewers rather than presented as a value automatically selected by the
model.

## The six topics (k=6)

### T1 — X-Minute City & Accessibility

**Top terms:** minute, accessibility, service, walking, within, mobility,
spatial, proximity, model, access

**Interpretation:** Labelled "X-Minute" rather than "15-Minute": numeric
prefixes are stripped during text cleaning, so this topic aggregates all
X-minute-city variants (15-, 20-, 10-, 30-minute, and explicit "X-minute"
framings), not only the 15-minute instantiation. Within the corpus,
15-minute is the dominant *specific* threshold discussed (897 of ~971
numeric mentions, ≈92%), so it is fair to describe 15-minute as the
dominant variant — but the topic label should not claim a precision the
underlying token does not carry.

### T2 — Compact City Policy & Residential Form

**Top terms:** compact, density, policy, travel, resident, social,
residential, high, transport, form

**Interpretation:** Normative/policy-oriented compact-city literature,
connected to residential density and travel behaviour.

### T3 — Urban Form, Density & Emissions

**Top terms:** compact, land, form, spatial, density, sustainable, model,
energy, emission, sustainability

**Interpretation:** The more quantitative/morphological compact-city
literature. Direct term-loading checks confirm pollution/emission/air-
quality terms load here, not on the walkability/health topic (T6) — i.e.
environmental exposure research travels with urban-form/density research
in this corpus, not with individual walkability-and-wellbeing research.
This is a substantive empirical finding: a combined "Health, Wellbeing &
Urban Environment" topic (as in the original conference presentation) does
not hold together in this corpus. Walkability/health and pollution/
emissions are two separate clusters.

### T4 — Sustainable Design & Policy Strategy

**Top terms:** concept, sustainable, policy, minute, design, strategy, new,
social, space, need

**Interpretation:** Overlaps partially with T1 (shares "minute") and with
T2/T3 (shares "sustainable", "policy") — reflecting genuine conceptual
overlap in the literature between X-minute city framing and broader
sustainable urban design discourse, rather than a modelling artifact.

### T5 — Housing, Green Space & Landscape

**Top terms:** housing, space, green, social, landscape, park, new,
compact, high, density

**Interpretation:** Smallest topic by dominant-document count (n=50) —
housing and green/park space provision literature.

### T6 — Walkability & Health

**Top terms:** walkability, environment, health, street, walkable, design,
physical, activity, built, pedestrian

**Interpretation:** A genuinely coherent cluster — physical activity,
mental health, and walkable design terms load together, confirmed via
direct term-loading checks rather than assumed from co-occurrence in the
top-10 list alone. This pairing holds up statistically, unlike the
pollution/emissions pairing discussed under T3 above.

## Co-occurrence network

An earlier network construction (restricting to the "top N terms by
weighted degree") produced a 98.8%-dense, near-complete graph, an outcome
that is guaranteed by that selection method regardless of the corpus's true
community structure, and so cannot be used as evidence of network
structure. The network reported here instead includes all terms passing a
document-frequency floor of 20 (independent of degree), with edges weighted
by Pointwise Mutual Information (PMI) and restricted to positive-PMI pairs
with a minimum co-occurrence count of 5 (see `scripts/cooccurrence_network.py`).

**Result:** 955 nodes, 75,330 edges, 16.5% density, 4 Louvain communities,
modularity Q = 0.1764.

**Significance:** tested against 20 degree-preserving randomizations
(`scripts/network_significance.py`): null model mean Q = 0.1215
(SD = 0.0019), Z = 28.99, p < 0.0001. The observed community structure is
highly unlikely to
