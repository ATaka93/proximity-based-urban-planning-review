"""
temporal_analysis.py

Step 6 of the pipeline: temporal trend analysis (RQ3). Computes two things
that earlier steps do not:

  1. Topic dominance share per year — for each publication year, the
     proportion of documents whose dominant topic is each of the k topics.
  2. Keyword frequency per year — for a small set of manuscript-relevant
     keywords, frequency per 1,000 words of cleaned text, by year.

This directly supports RQ3 ("How have the dominant thematic groupings and
research emphases shifted over publication years?"), which the topic model
and network scripts alone do not address.

Input:  results/tokenized_corpus.csv (from preprocess.py; must retain a
        'year' column, carried through from data/abstracts.csv)
        results/lda_doc_topic.csv (from lda_model.py; one row per document,
        same row order as tokenized_corpus.csv)
Output: results/topic_share_by_year.csv
        results/keyword_frequency_by_year.csv
"""

import argparse
from pathlib import Path

import pandas as pd


def compute_topic_share_by_year(tokenized_df, doc_topic_df):
    """For each year, the proportion of documents whose dominant topic is
    each topic (i.e. the share of the year's corpus dominated by that
    topic), plus the raw document count that year."""
    if len(tokenized_df) != len(doc_topic_df):
        raise ValueError(
            f"Row count mismatch: tokenized_corpus.csv has {len(tokenized_df)} rows, "
            f"lda_doc_topic.csv has {len(doc_topic_df)} rows. These must be produced "
            f"from the same preprocess.py run to align correctly."
        )

    merged = pd.concat(
        [tokenized_df[["year"]].reset_index(drop=True),
         doc_topic_df[["dominant_topic"]].reset_index(drop=True)],
        axis=1,
    )

    counts = merged.groupby(["year", "dominant_topic"]).size().unstack(fill_value=0)
    shares = counts.div(counts.sum(axis=1), axis=0)
    shares["n_documents"] = counts.sum(axis=1)
    return shares.reset_index()


def compute_keyword_frequency_by_year(tokenized_df, keywords):
    """Frequency per 1,000 (cleaned, lemmatized) words, by year, for each
    keyword. Keywords should be given in their post-lemmatization form
    (e.g. 'minute' not '15-minute', since numeric prefixes and hyphens are
    stripped during preprocessing)."""
    rows = []
    for year, group in tokenized_df.groupby("year"):
        all_tokens = " ".join(group["cleaned"].astype(str)).split()
        total_words = len(all_tokens)
        row = {"year": year, "total_words": total_words}
        for kw in keywords:
            count = all_tokens.count(kw)
            row[f"{kw}_per_1000_words"] = (count / total_words * 1000) if total_words else 0.0
        rows.append(row)
    return pd.DataFrame(rows).sort_values("year")


def main():
    parser = argparse.ArgumentParser(description="Compute topic-share and keyword-frequency trends by year.")
    parser.add_argument("--tokenized", default="results/tokenized_corpus.csv")
    parser.add_argument("--doc-topic", default="results/lda_doc_topic.csv")
    parser.add_argument("--outdir", default="results")
    parser.add_argument("--keywords", nargs="+",
                         default=["minute", "accessibility", "proximity", "equity", "walkability"],
                         help="Keywords to track (post-lemmatization form, no numeric prefixes).")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    tokenized_df = pd.read_csv(args.tokenized)
    if "year" not in tokenized_df.columns:
        raise ValueError(
            "tokenized_corpus.csv must contain a 'year' column. "
            "Ensure data/abstracts.csv has a 'year' column before running preprocess.py."
        )
    doc_topic_df = pd.read_csv(args.doc_topic)

    print(f"Computing topic share by year across {len(tokenized_df)} documents...")
    topic_share_df = compute_topic_share_by_year(tokenized_df, doc_topic_df)
    topic_share_df.to_csv(outdir / "topic_share_by_year.csv", index=False)
    print(topic_share_df.to_string(index=False))

    print(f"\nComputing keyword frequency by year for: {args.keywords}")
    keyword_freq_df = compute_keyword_frequency_by_year(tokenized_df, args.keywords)
    keyword_freq_df.to_csv(outdir / "keyword_frequency_by_year.csv", index=False)
    print(keyword_freq_df.to_string(index=False))

    print(f"\nSaved to {outdir}/topic_share_by_year.csv and {outdir}/keyword_frequency_by_year.csv")


if __name__ == "__main__":
    main()
