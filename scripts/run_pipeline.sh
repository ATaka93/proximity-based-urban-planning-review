# run_pipeline.sh
#
# Runs the full analysis pipeline end to end, in order:
#   1. preprocess.py             -> results/dtm.npz, vocabulary.csv, tokenized_corpus.csv
#   2. model_selection.py        -> results/model_selection_perplexity.csv, model_selection_coherence.csv
#   3. lda_model.py               -> results/lda_topic_term.csv, lda_doc_topic.csv, lda_model.joblib
#   4. cooccurrence_network.py    -> results/cooccurrence_edges_pmi.csv, network_communities_pmi.csv
#   5. network_significance.py    -> results/network_significance.txt
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

echo "=== Step 1/5: Pre-processing and DTM construction ==="
python3 scripts/preprocess.py --input "$INPUT" --outdir "$OUTDIR"

echo ""
echo "=== Step 2/5: Statistical model selection
