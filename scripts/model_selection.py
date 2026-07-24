"""
model_selection.py

Statistical justification for the choice of k (number of LDA topics).
Reports two metrics across a range of k:

  1. Held-out perplexity (lower = better held-out fit, via sklearn).
     Perplexity is a known weak proxy for topic interpretability (Chang et
     al., 2009, "Reading Tea Leaves: How Humans Interpret Topic Models" -
     held-out likelihood often does not track human judgments of topic
     quality).
  2. Topic coherence (c_v, via gensim), which correlates better with human
     interpretability and is the standard metric for this kind of decision
     in the topic-modelling literature.

Both are reported together rather than only the metric that favours a
preferred k, since the two can disagree and that disagreement is itself
informative for the choice of k.

Input:  results/dtm.npz, results/vocabulary.csv, results/tokenized_corpus.csv
Output: results/model_selection_perplexity.csv
        results/model_selection_coherence.csv
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from scipy import sparse
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.model_selection import train_test_split


def run_perplexity_scan(dtm, k_range, max_iter=30, test_size=0.2, random_state=42):
    train_idx, test_idx = train_test_split(
        np.arange(dtm.shape[0]), test_size=test_size, random_state=random_state
    )
    dtm_train, dtm_test = dtm[train_idx], dtm[test_idx]

    rows = []
    for k in k_range:
        lda = LatentDirichletAllocation(
            n_components=k, max_iter=max_iter, random_state=random_state, learning_method="batch"
        )
        lda.fit(dtm_train)
        rows.append({
            "k": k,
            "log_likelihood": lda.score(dtm_test),
            "perplexity": lda.perplexity(dtm_test),
        })
    return pd.DataFrame(rows)


def run_coherence_scan(texts, k_range, min_df=5, max_df=0.90, passes=10, iterations=30, random_state=42):
    dictionary = Dictionary(texts)
    dictionary.filter_extremes(no_below=min_df, no_above=max_df)
    corpus = [dictionary.doc2bow(text) for text in texts]

    rows = []
    for k in k_range:
        lda = LdaModel(
            corpus=corpus, id2word=dictionary, num_topics=k,
            random_state=random_state, passes=passes, iterations=iterations
        )
        cm = CoherenceModel(model=lda, texts=texts, dictionary=dictionary, coherence="c_v")
        rows.append({"k": k, "coherence_cv": cm.get_coherence()})
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description="Statistically evaluate candidate values of k for LDA topic modelling.")
    parser.add_argument("--dtm", default="results/dtm.npz")
    parser.add_argument("--tokenized", default="results/tokenized_corpus.csv")
    parser.add_argument("--outdir", default="results")
    parser.add_argument("--k-min", type=int, default=3)
    parser.add_argument("--k-max", type=int, default=10)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    k_range = list(range(args.k_min, args.k_max + 1))

    dtm = sparse.load_npz(args.dtm)
    perplexity_df = run_perplexity_scan(dtm, k_range)
    perplexity_df.to_csv(outdir / "model_selection_perplexity.csv", index=False)
    print("Held-out perplexity by k (lower = better held-out fit):")
    print(perplexity_df.to_string(index=False))
    best_perplexity_k = perplexity_df.loc[perplexity_df["perplexity"].idxmin(), "k"]
    print(f"Lowest perplexity at k={int(best_perplexity_k)}\n")

    tc = pd.read_csv(args.tokenized)
    texts = [str(doc).split() for doc in tc["cleaned"].tolist()]
    coherence_df = run_coherence_scan(texts, k_range)
    coherence_df.to_csv(outdir / "model_selection_coherence.csv", index=False)
    print("Topic coherence (c_v) by k (higher = better interpretability):")
    print(coherence_df.to_string(index=False))
    best_coherence_k = coherence_df.loc[coherence_df["coherence_cv"].idxmax(), "k"]
    print(f"Highest coherence at k={int(best_coherence_k)}")

    print(f"\nSaved to {outdir}/model_selection_perplexity.csv and {outdir}/model_selection_coherence.csv")


if __name__ == "__main__":
    main()
