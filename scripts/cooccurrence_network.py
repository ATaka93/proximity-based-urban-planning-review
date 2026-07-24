"""
cooccurrence_network.py

Step 5 of the pipeline: term co-occurrence network construction and Louvain
community detection.

Edges are weighted by Pointwise Mutual Information (PMI) rather than raw
co-occurrence counts, so an edge reflects terms that co-occur more often
than chance, not simply high-frequency terms co-occurring by sheer volume.
Only positive-PMI edges are kept (i.e. co-occurring more than expected
under independence), with a minimum raw co-occurrence count to avoid noise
from rare term pairs. Candidate nodes are all terms passing a document-
frequency floor, independent of their eventual network degree, so that
node inclusion does not bias the network toward artificially high density.

Input:  results/tokenized_corpus.csv  (from preprocess.py; uses the 'cleaned'
        column of lemmatized, whitespace-joined tokens)
Output: results/cooccurrence_edges_pmi.csv   (edge list: term_a, term_b, pmi, co_occurrence_count)
        results/network_communities_pmi.csv  (term -> community assignment)
        results/network_summary_pmi.txt      (node/edge/density/modularity summary)
"""

import argparse
from collections import Counter
from itertools import combinations
from pathlib import Path

import community as community_louvain
import networkx as nx
import numpy as np
import pandas as pd


def build_pmi_network(docs, min_doc_freq=20, min_co_occurrence=5):
    """Build a PMI-weighted co-occurrence network.

    docs: list of sets of tokens, one set per document.
    min_doc_freq: minimum number of documents a term must appear in to be
        considered a candidate node.
    min_co_occurrence: minimum raw co-occurrence count for an edge, to avoid
        PMI being dominated by noise from rare term pairs.
    """
    n_docs = len(docs)

    term_doc_freq = Counter()
    for doc in docs:
        term_doc_freq.update(doc)
    candidate_terms = {t for t, c in term_doc_freq.items() if c >= min_doc_freq}

    pair_counts = Counter()
    for doc in docs:
        terms_in_doc = sorted(doc & candidate_terms)
        for a, b in combinations(terms_in_doc, 2):
            pair_counts[(a, b)] += 1

    edges = []
    for (a, b), co_count in pair_counts.items():
        if co_count < min_co_occurrence:
            continue
        p_a = term_doc_freq[a] / n_docs
        p_b = term_doc_freq[b] / n_docs
        p_ab = co_count / n_docs
        pmi = np.log(p_ab / (p_a * p_b))
        if pmi > 0:
            edges.append((a, b, pmi, co_count))

    edges_df = pd.DataFrame(edges, columns=["term_a", "term_b", "pmi", "co_occurrence_count"])
    return edges_df, candidate_terms


def main():
    parser = argparse.ArgumentParser(description="Build a PMI-weighted co-occurrence network and detect communities.")
    parser.add_argument("--input", default="results/tokenized_corpus.csv")
    parser.add_argument("--outdir", default="results")
    parser.add_argument("--min-doc-freq", type=int, default=20,
                         help="Minimum document frequency for a term to be a candidate node.")
    parser.add_argument("--min-co-occurrence", type=int, default=5,
                         help="Minimum raw co-occurrence count for an edge.")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)
    if "cleaned" not in df.columns:
        raise ValueError("Input CSV must contain a 'cleaned' column (from preprocess.py).")

    docs = [set(str(doc).split()) for doc in df["cleaned"].tolist()]

    print(f"Building PMI-weighted co-occurrence network from {len(docs)} documents "
          f"(min doc freq >= {args.min_doc_freq}, min co-occurrence >= {args.min_co_occurrence})")

    edges_df, candidate_terms = build_pmi_network(
        docs, min_doc_freq=args.min_doc_freq, min_co_occurrence=args.min_co_occurrence
    )
    print(f"Candidate terms: {len(candidate_terms)}")

    if edges_df.empty:
        print("WARNING: no edges met the criteria. Try lowering --min-doc-freq or --min-co-occurrence.")
        return

    edges_df.to_csv(outdir / "cooccurrence_edges_pmi.csv", index=False)

    graph = nx.from_pandas_edgelist(edges_df, "term_a", "term_b", edge_attr="pmi")
    density = graph.number_of_edges() / (graph.number_of_nodes() * (graph.number_of_nodes() - 1) / 2)

    partition = community_louvain.best_partition(graph, weight="pmi", random_state=42)
    modularity = community_louvain.modularity(partition, graph, weight="pmi")
    n_communities = len(set(partition.values()))

    communities_df = pd.DataFrame(
        [(term, comm_id) for term, comm_id in partition.items()],
        columns=["term", "community"],
    ).sort_values(["community", "term"])
    communities_df.to_csv(outdir / "network_communities_pmi.csv", index=False)

    summary = (
        f"Nodes: {graph.number_of_nodes()}\n"
        f"Edges: {graph.number_of_edges()}\n"
        f"Density: {density:.4f}\n"
        f"Communities detected: {n_communities}\n"
        f"Modularity (Q): {modularity:.4f}\n"
        f"\nRun network_significance.py to test whether this modularity is\n"
        f"statistically significant against a degree-preserving random null model.\n"
    )
    (outdir / "network_summary_pmi.txt").write_text(summary)

    print(f"Nodes: {graph.number_of_nodes()}, Edges: {graph.number_of_edges()}, Density: {density:.1%}")
    print(f"Communities: {n_communities}, Modularity (Q): {modularity:.4f}")
    print(f"Saved edge list, community assignments, and summary to {outdir}/")


if __name__ == "__main__":
    main()
