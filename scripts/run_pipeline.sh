#!/usr/bin/env bash
# run_pipeline.sh
#
# Runs the full analysis pipeline end to end, in order:
#   1. preprocess.py             -> results/dtm.npz, vocabulary.csv, tokenized_corpus.csv
#   2. model_selection.py        -> results/model_selection_perplexity.csv, model_selection_coherence.csv
#   3. lda_model.py               -> results/lda_topic_term.csv, lda_doc_topic.csv, lda_model.joblib
#   4. cooccurrence_network.py    -> results/cooccurrence_edges_pmi.csv, network_communities_pmi.csv
#   5. network_significance.py    -> results/network_significance.txt
#   6. temporal_analysis.py       -> results/topic_share_by_year.csv, keyword_frequency_by_year.csv
#   7. generate_figures.py        -> figures/fig1_topic_share_by_year.png, fig2_keyword_frequency_by_year.png,
#                                     fig3_cooccurrence_network.png, fig4_model_selection.png
#
# Usage:
#   bash scripts/run_pipeline.sh
#
# Assumes:
#   - dependencies installed from requirements.txt
#   - input file at data/abstracts.csv with an 'abstract' column
#     (see data/README.md for how to obtain/reconstruct this corpus)

set -euo pipefail

INPUT="${1:-data/abstracts.csv}"
OUTDIR="${2:-results}"

echo "=== Step 1/7: Pre-processing and DTM construction ==="
python3 scripts/preprocess.py --input "$INPUT" --outdir "$OUTDIR"

echo ""
echo "=== Step 2/7: Statistical model selection (evaluating k) ==="
python3 scripts/model_selection.py --dtm "$OUTDIR/dtm.npz" --tokenized "$OUTDIR/tokenized_corpus.csv" --outdir "$OUTDIR"

echo ""
echo "=== Step 3/7: LDA topic modelling (k=6, 30 iterations) ==="
python3 scripts/lda_model.py --dtm "$OUTDIR/dtm.npz" --vocab "$OUTDIR/vocabulary.csv" --outdir "$OUTDIR"

echo ""
echo "=== Step 4/7: PMI-weighted co-occurrence network + Louvain communities ==="
python3 scripts/cooccurrence_network.py --input "$OUTDIR/tokenized_corpus.csv" --outdir "$OUTDIR"

echo ""
echo "=== Step 5/7: Network modularity significance testing ==="
python3 scripts/network_significance.py --edges "$OUTDIR/cooccurrence_edges_pmi.csv" --outdir "$OUTDIR"

echo ""
echo "=== Step 6/7: Temporal trend analysis (topic share & keyword frequency by year) ==="
python3 scripts/temporal_analysis.py --tokenized "$OUTDIR/tokenized_corpus.csv" --doc-topic "$OUTDIR/lda_doc_topic.csv" --outdir "$OUTDIR"

echo ""
echo "=== Step 7/7: Generating figures ==="
python3 scripts/generate_figures.py --results-dir "$OUTDIR" --outdir figures

echo ""
echo "=== Pipeline complete. Outputs written to $OUTDIR/ and figures/ ==="
