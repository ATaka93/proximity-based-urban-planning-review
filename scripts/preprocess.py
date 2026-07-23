"""
preprocess.py

Step 3 of the pipeline: text pre-processing and document-term matrix (DTM)
construction.

Input:  data/abstracts.csv  (must contain a column named 'abstract'; an
        optional 'year' column is preserved for later temporal analysis)
Output: results/dtm.npz             (sparse document-term matrix)
        results/vocabulary.csv       (feature/term list, index-aligned to DTM columns)
        results/tokenized_corpus.csv (cleaned, lemmatized text per document)

Parameters (fixed to match the values reported in docs/prisma-protocol.md
and the manuscript methodology):
    CountVectorizer: max_df=0.90, min_df=5
"""

import argparse
import re
from pathlib import Path

import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer

REQUIRED_NLTK = ["punkt", "punkt_tab", "stopwords", "wordnet"]
for pkg in REQUIRED_NLTK:
    try:
        nltk.data.find(
            f"tokenizers/{pkg}" if "punkt" in pkg else f"corpora/{pkg}"
        )
    except LookupError:
        nltk.download(pkg, quiet=True)

STOPWORDS = set(stopwords.words("english"))
# Domain-specific stopwords: high-frequency but analytically uninformative
# terms in this corpus (adjust as needed for your own screening).
DOMAIN_STOPWORDS = {"study", "paper", "research", "article", "result", "findings"}
STOPWORDS |= DOMAIN_STOPWORDS

LEMMATIZER = WordNetLemmatizer()


def clean_and_lemmatize(text: str) -> str:
    """Lowercase, strip non-alphabetic tokens, remove stopwords, lemmatize."""
    text = text.lower()
    text = re.sub(r"[^a-z\s-]", " ", text)
    tokens = word_tokenize(text)
    tokens = [
        LEMMATIZER.lemmatize(tok)
        for tok in tokens
        if tok not in STOPWORDS and len(tok) > 2
    ]
    return " ".join(tokens)


def build_dtm(cleaned_texts, max_df=0.90, min_df=5):
    """Build a document-term matrix using CountVectorizer with the
    parameters reported in the manuscript methodology."""
    vectorizer = CountVectorizer(max_df=max_df, min_df=min_df)
    dtm = vectorizer.fit_transform(cleaned_texts)
    vocabulary = vectorizer.get_feature_names_out()
    return dtm, vocabulary, vectorizer


def main():
    parser = argparse.ArgumentParser(description="Pre-process abstracts and build a DTM.")
    parser.add_argument("--input", default="data/abstracts.csv",
                         help="Path to CSV with an 'abstract' column.")
    parser.add_argument("--outdir", default="results",
                         help="Directory to write outputs to.")
    parser.add_argument("--max-df", type=float, default=0.90)
    parser.add_argument("--min-df", type=int, default=5)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)
    if "abstract" not in df.columns:
        raise ValueError("Input CSV must contain an 'abstract' column.")

    print(f"Loaded {len(df)} records from {args.input}")

    df["cleaned"] = df["abstract"].astype(str).apply(clean_and_lemmatize)

    dtm, vocabulary, _ = build_dtm(df["cleaned"], max_df=args.max_df, min_df=args.min_df)

    print(f"DTM shape: {dtm.shape[0]} documents x {dtm.shape[1]} terms")

    sparse.save_npz(outdir / "dtm.npz", dtm)
    pd.Series(vocabulary, name="term").to_csv(outdir / "vocabulary.csv", index=False)
    df.to_csv(outdir / "tokenized_corpus.csv", index=False)

    print(f"Saved DTM, vocabulary, and tokenized corpus to {outdir}/")


if __name__ == "__main__":
    main()
