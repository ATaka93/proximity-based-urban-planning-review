"""
cooccurrence_network.py

Step 5 of the pipeline: term co-occurrence network construction and Louvain
community detection.

Input:  results/tokenized_corpus.csv  (from preprocess.py; uses the 'cleaned'
        column of lemmatized, whitespace-joined tokens)
Output: results/cooccurrence_edges.csv    (edge list with weights)
        results/network_communities.csv   (term -> community assignment)
        results/network_summary.txt       (node/edge counts, modularity)

Parameters (fixed to match docs/prisma-protocol.md / manuscript methodology):
    Co-occurrence threshold: edges retained only where co-occurrence count n >= 20
    Community detection: Louvain algorithm (python-louvain)
"""

import argparse
from itertools import combinations
from pathlib import Path

import community as community_louvain
import networkx as nx
import pandas as pd


def build_cooccurrence_graph(tokenized_docs, threshold=20):
    """Count how often each pair of terms co-occurs within the same
    document, then keep only edges at or above the threshold."""
    pair_counts = {}
    for doc in tokenized_docs:
        terms = sorted(set(doc.split()))
        for term_a, term_b in combinations(terms, 2):
            key = (term_a, term_b)
            pair_counts[key] = pair_counts.get(key, 0) + 1

    graph = nx.Graph()
    for (term_a, term_b), weight in pair_counts.items():
        if weight >= threshold:
            graph.add_edge(term_a, term_b, weight=weight)

    return graph


def main():
    parser = argparse.ArgumentParser(description="Build a term co-occurrence network and detect communities.")
    parser.add_argument("--input", default="results/tokenized_corpus.csv")
    parser.add_argument("--outdir", default="results")
    parser.add_argument("--threshold", type=int, default=20,
                         help="Minimum co-occurrence count for an edge to be kept.")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(args.input)
    if "cleaned" not in df.columns:
        raise ValueError("Input CSV must contain a 'cleaned' column (from preprocess.py).")

    tokenized_docs = df["cleaned"].astype(str).tolist()

    print(f"Building co-occurrence network from {len(tokenized_docs)} documents "
          f"(edge threshold n >= {args.threshold})")

    graph = build_cooccurrence_graph(tokenized_docs, threshold=args.threshold)

    if graph.number_of_nodes() == 0:
        print("WARNING: no edges met the threshold. Try lowering --threshold "
              "(e.g. for a small test corpus).")
        return

    partition = community_louvain.best_partition(graph, weight="weight", random_state=42)
    modularity = community_louvain.modularity(partition, graph, weight="weight")

    edges_df = pd.DataFrame(
        [(u, v, d["weight"]) for u, v, d in graph.edges(data=True)],
        columns=["term_a", "term_b", "weight"],
    ).sort_values("weight", ascending=False)
    edges_df.to_csv(outdir / "cooccurrence_edges.csv", index=False)

    communities_df = pd.DataFrame(
        [(term, comm_id) for term, comm_id in partition.items()],
        columns=["term", "community"],
    ).sort_values(["community", "term"])
    communities_df.to_csv(outdir / "network_communities.csv", index=False)

    n_communities = communities_df["community"].nunique()
    summary = (
        f"Nodes: {graph.number_of_nodes()}\n"
        f"Edges: {graph.number_of_edges()}\n"
        f"Communities detected: {n_communities}\n"
        f"Modularity (Q): {modularity:.4f}\n"
    )
    (outdir / "network_summary.txt").write_text(summary)

    print(summary)
    print(f"Saved edge list and community assignments to {outdir}/")


if __name__ == "__main__":
    main()
