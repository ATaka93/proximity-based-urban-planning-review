"""
lda_model.py

Step 4 of the pipeline: LDA topic modelling.

Input:  results/dtm.npz           (from preprocess.py)
        results/vocabulary.csv    (from preprocess.py)
Output: results/lda_topic_term.csv     (top terms per topic)
        results/lda_doc_topic.csv      (per-document topic distribution)
        results/lda_model.joblib       (fitted model, for reuse)

Parameters (fixed to match docs/prisma-protocol.md / manuscript methodology):
    LDA: scikit-learn, n_components=6, max_iter=30
"""

import argparse
from pathlib import Path

import joblib
import pandas as pd
from scipy import sparse
from sklearn.decomposition import LatentDirichletAllocation


def fit_lda(dtm, n_topics=6, max_iter=30, random_state=42):
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        max_iter=max_iter,
        random_state=random_state,
        learning_method="batch",
    )
    doc_topic = lda.fit_transform(dtm)
    return lda, doc_topic


def top_terms_per_topic(lda, vocabulary, n_top_words=10):
    rows = []
    for topic_idx, topic in enumerate(lda.components_):
        top_indices = topic.argsort()[::-1][:n_top_words]
        for rank, idx in enumerate(top_indices, start=1):
            rows.append({
                "topic": f"T{topic_idx + 1}",
                "rank": rank,
                "term": vocabulary[idx],
                "weight": topic[idx],
            })
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description="Fit an LDA topic model to the DTM.")
    parser.add_argument("--dtm", default="results/dtm.npz")
    parser.add_argument("--vocab", default="results/vocabulary.csv")
    parser.add_argument("--outdir", default="results")
    parser.add_argument("--n-topics", type=int, default=6)
    parser.add_argument("--max-iter", type=int, default=30)
    parser.add_argument("--top-words", type=int, default=10,
                         help="Number of top terms to report per topic.")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    dtm = sparse.load_npz(args.dtm)
    vocabulary = pd.read_csv(args.vocab)["term"].tolist()

    print(f"Fitting LDA: k={args.n_topics}, max_iter={args.max_iter}, "
          f"on {dtm.shape[0]} documents x {dtm.shape[1]} terms")

    lda, doc_topic = fit_lda(dtm, n_topics=args.n_topics, max_iter=args.max_iter)

    topic_term_df = top_terms_per_topic(lda, vocabulary, n_top_words=args.top_words)
    topic_term_df.to_csv(outdir / "lda_topic_term.csv", index=False)

    doc_topic_df = pd.DataFrame(
        doc_topic, columns=[f"T{i + 1}" for i in range(args.n_topics)]
    )
    doc_topic_df["dominant_topic"] = doc_topic_df.idxmax(axis=1)
    doc_topic_df.to_csv(outdir / "lda_doc_topic.csv", index=False)

    joblib.dump(lda, outdir / "lda_model.joblib")

    print(f"Saved topic-term table, doc-topic distributions, and fitted model to {outdir}/")
    print("\nTop terms per topic:")
    for topic_id in topic_term_df["topic"].unique():
        terms = topic_term_df[topic_term_df["topic"] == topic_id]["term"].tolist()
        print(f"  {topic_id}: {', '.join(terms[:5])}")


if __name__ == "__main__":
    main()
