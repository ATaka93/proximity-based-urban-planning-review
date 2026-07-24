"""
network_significance.py

Tests whether the co-occurrence network's community structure (modularity Q)
is statistically significant, rather than assuming a low or high Q value
is meaningful on its own. Modularity is only interpretable relative to a
null model: this script compares observed Q against Q computed on
degree-preserving randomizations (configuration-model-style rewiring via
double_edge_swap), which destroy any genuine community structure while
preserving the degree sequence.

Input:  results/cooccurrence_edges_pmi.csv (from cooccurrence_network.py)
Output: results/network_significance.txt
        results/network_modularity_null_distribution.csv

Note: this is computationally expensive for large/dense networks (each
permutation refits Louvain community detection), so the default number of
permutations is kept modest (20) for tractability. Increase
--n-permutations for a more precise p-value if compute time allows.
"""

import argparse
import time
from pathlib import Path

import community as community_louvain
import networkx as nx
import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Test statistical significance of network modularity.")
    parser.add_argument("--edges", default="results/cooccurrence_edges_pmi.csv")
    parser.add_argument("--outdir", default="results")
    parser.add_argument("--n-permutations", type=int, default=20)
    parser.add_argument("--nswap", type=int, default=5000,
                         help="Number of edge swaps per randomization (degree-preserving rewiring).")
    parser.add_argument("--max-tries", type=int, default=50000)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    edges_df = pd.read_csv(args.edges)
    graph = nx.from_pandas_edgelist(edges_df, "term_a", "term_b", edge_attr="pmi")

    partition = community_louvain.best_partition(graph, weight="pmi", random_state=args.random_state)
    observed_q = community_louvain.modularity(partition, graph, weight="pmi")
    n_communities = len(set(partition.values()))

    print(f"Observed network: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
    print(f"Observed communities: {n_communities}, modularity Q: {observed_q:.4f}")
    print(f"Running {args.n_permutations} degree-preserving randomizations...")

    np.random.seed(args.random_state)
    null_qs = []
    t0 = time.time()
    for i in range(args.n_permutations):
        try:
            graph_rand = nx.double_edge_swap(
                graph.copy(), nswap=args.nswap, max_tries=args.max_tries, seed=i
            )
            partition_rand = community_louvain.best_partition(
                graph_rand, weight="pmi", random_state=args.random_state
            )
            null_qs.append(community_louvain.modularity(partition_rand, graph_rand, weight="pmi"))
        except nx.NetworkXAlgorithmError:
            continue

    elapsed = time.time() - t0
    null_qs = np.array(null_qs)
    print(f"{len(null_qs)} successful permutations in {elapsed:.1f}s")

    if len(null_qs) < 2:
        print("WARNING: too few successful permutations to compute a meaningful null distribution.")
        return

    z_score = (observed_q - null_qs.mean()) / null_qs.std()
    p_value = (null_qs >= observed_q).mean()

    print(f"Null model mean Q: {null_qs.mean():.4f} (SD={null_qs.std():.4f})")
    print(f"Z-score: {z_score:.2f}")
    print(f"Empirical p-value: {p_value:.4f}")

    pd.DataFrame({"null_Q": null_qs}).to_csv(outdir / "network_modularity_null_distribution.csv", index=False)

    summary = (
        f"Observed modularity Q: {observed_q:.4f}\n"
        f"Observed communities: {n_communities}\n"
        f"Null model permutations: {len(null_qs)}\n"
        f"Null model mean Q: {null_qs.mean():.4f} (SD={null_qs.std():.4f})\n"
        f"Z-score: {z_score:.2f}\n"
        f"Empirical p-value: {p_value:.4f}\n"
    )
    (outdir / "network_significance.txt").write_text(summary)
    print(f"\nSaved significance test results to {outdir}/network_significance.txt")


if __name__ == "__main__":
    main()
