# PRISMA Protocol

## Search strategy

- Databases: Web of Science, Scopus
- Search field: Abstract (AB=)
- Filters applied:
  - Language: English
  - Document types: Article, Review Article
- Date range: 1992–2026
- Records identified (raw, combined WoS + Scopus, pre-deduplication): 3,942

Search syntax:
AB=("minute* cit*" OR "compact cit*" OR "walkable cit*" OR "proximity-based cit*"
OR "self-sufficient cit*" OR "minute* urban*" OR "compact urban*" OR "walkable urban*"
OR "proximity-based urban*" OR "self-sufficient urban*" OR "chrono-urbanism")

## Deduplication

- Cross-database duplicates (Web of Science ∩ Scopus) were identified and
  removed prior to screening.
- Duplicate records removed: 1,576
- Records after deduplication, proceeding to abstract screening: 2,366

## Screening

Screening was conducted at the abstract level only, without a separate
title-screening or full-text-screening stage. This choice reflects the aims
of the study: because the objective was to map conceptual and terminological
trends in the proximity-based urban planning literature — rather than to
assess methodological quality or extract detailed empirical results —
abstracts, which typically state a publication's core concepts, terminology,
and research questions, provided sufficient information to determine topical
relevance. Abstract-level screening is also consistent with the text-analytic
design of the study, which itself relies on abstract text as the primary
corpus (see Text Pre-processing and LDA Topic Modelling in the main
manuscript). Full-text screening was additionally impractical given that not
all identified records were accessible without subscription or payment.

- Inclusion/exclusion criteria: records were retained only if their abstract
  empirically addresses a neighbourhood-scale, proximity-based, or
  X-minute/15-minute city planning concept — i.e. it operationalises or
  measures access to daily services, amenities, or functions within a
  defined time/distance threshold or through explicit X-minute city
  components.
- Records excluded at the abstract-screening stage were each assigned a
  specific reason. The full, per-record reason is logged in
  `exclusion-log.md`. Recurring categories of exclusion include:

  | Exclusion category | Description |
  |---|---|
  | No neighbourhood-scale accessibility/proximity component | City-, regional-, or macro-scale studies (e.g. carbon emissions, land-use change, urban sprawl, compactness metrics) that do not operationalise access to daily services or X-minute city components |
  | Environmental/climate/thermal focus only | Urban heat island, microclimate, thermal comfort, or air-quality studies with no accessibility or proximity dimension |
  | Conceptual/theoretical/discursive only | Political, critical, or discourse-analytic treatments of the 15-minute city that do not define or measure components empirically |
  | Compact city as contextual label only | Studies that use "compact city" descriptively (e.g. as a study-area label) without analysing it as an urban form or proximity model |
  | Off-topic / unrelated discipline | Medical, engineering, materials-science, or other studies unrelated to urban form or accessibility |
  | Transport/mobility without X-minute framing | Transit, travel-behaviour, or mobility studies not framed around neighbourhood-scale service access |
  | Ecology/biodiversity/green space without accessibility | Environmental or ecological studies of green space, habitat, or vegetation without a service-access or proximity framework |

- Records excluded: 1,339
- Records included: 1,027

## Limitations of the screening approach

Because eligibility was determined at the abstract level, some borderline
records may have been mis-classified relative to their full-text content.
This risk is mitigated by the specificity of the search syntax and the
exploratory, corpus-level nature of the analysis, which aims to characterise
broad conceptual trends rather than to make claims about individual studies'
findings or methodological quality.

## PRISMA flow diagram

Summary of the flow:
Records identified (WoS + Scopus, combined): 3,942
| duplicates removed: 1,576
v
Records screened by abstract: 2,366
| excluded at abstract screening: 1,339
v
Records included in final corpus: 1,027

See `prisma-flow-diagram.png` in this folder for the visual version of this
flow, formatted per PRISMA 2020 guidelines.

## Topic labelling

Six latent topics (T1–T6) were identified via LDA (k=6) on the final corpus
of 1,027 records. See `topic-codebook.md` in this folder for the
interpretive labels assigned to each topic, the top terms used to justify
each label, and the statistical justification for k=6.
