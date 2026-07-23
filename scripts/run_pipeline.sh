#!/usr/bin/env bash
# run_pipeline.sh
#
# Runs the full analysis pipeline end to end, in order:
#   1. preprocess.py            -> results/dtm.npz, vocabulary.csv, tokenized_corpus.csv
#   2. lda_model.py              -> results/lda_topic_term.csv, lda_doc_topic.csv, lda_model.joblib
#   3. cooccurrence_network.py   -> results/cooccurrence_edges.csv, network_communities.csv
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

echo "=== Step 1/3: Pre-processing and DTM construction ==="
python3 scripts/preprocess.py --input "$INPUT" --outdir "$OUTDIR"

echo ""
echo "=== Step 2/3: LDA topic modelling (k=6, 30 iterations) ==="
python3 scripts/lda_model.py --dtm "$OUTDIR/dtm.npz" --vocab "$OUTDIR/vocabulary.csv" --outdir "$OUTDIR"

echo ""
echo "=== Step 3/3: Co-occurrence network + Louvain communities (threshold n>=20) ==="
python3 scripts/cooccurrence_network.py --input "$OUTDIR/tokenized_corpus.csv" --outdir "$OUTDIR"

echo ""
echo "=== Pipeline complete. Outputs written to $OUTDIR/ ==="
