"""
generate_figures.py

Step 7 of the pipeline: generates the manuscript figures from the pipeline's
result files. Produces:

  fig1_topic_share_by_year.png       - stacked area chart of topic dominance by year
  fig2_keyword_frequency_by_year.png - line chart of keyword frequency trends
  fig3_cooccurrence_network.png      - network diagram (top 60 terms by weighted
                                        degree, for legibility; full-network
                                        statistics are reported in the caption)
  fig4_model_selection.png           - perplexity/coherence by k, showing the
                                        k=6 justification and trade-off

Input:  results/topic_share_by_year.csv
        results/keyword_frequency_by_year.csv
        results/cooccurrence_edges_pmi.csv
        results/network_communities_pmi.csv
        results/model_selection_perplexity.csv
        results/model_selection_coherence.csv
Output: figures/fig1_topic_share_by_year.png
        figures/fig2_keyword_frequency_by_year.png
        figures/fig3_cooccurrence_network.png
        figures/fig4_model_selection.png
"""

import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

mpl.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "figure.dpi": 300})

TOPIC_LABELS = {
    "T1": "X-Minute City &\nAccessibility",
    "T2": "Compact City Policy &\nResidential Form",
    "T3": "Urban Form, Density\n& Emissions",
    "T4": "Sustainable Design &\nPolicy Strategy",
    "T5": "Housing, Green Space\n& Landscape",
    "T6": "Walkability & Health",
}
TOPIC_COLORS = ["#2C5FA8", "#B23B3B", "#2E7D45", "#B8860B", "#7B5EA7", "#3B8F9E"]

COMMUNITY_LABELS = {
    0: "X-Minute City, Proximity\n& Accessibility",
    1: "Neighbourhood &\nResidential Density",
    2: "Walkability, Active\nTravel & Health",
    3: "Sustainability &\nPolicy Strategy",
}
COMMUNITY_COLORS = {0: "#2C5FA8", 1: "#B8860B", 2: "#2E7D45", 3: "#7B5EA7"}


def fig1_topic_share(outdir, results_dir, min_docs=5):
    df = pd.read_csv(results_dir / "topic_share_by_year.csv")
    df = df[df["n_documents"] >= min_docs].sort_values("year")
    topics = [t for t in TOPIC_LABELS if t in df.columns]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.stackplot(df["year"], [df[t] for t in topics],
                 labels=[TOPIC_LABELS[t] for t in topics], colors=TOPIC_COLORS, alpha=0.88)
    ax.set_xlabel("Publication year")
    ax.set_ylabel("Share of documents (dominant topic)")
    ax.set_title(f"Topic dominance share by publication year\n"
                 f"(years with \u2265{min_docs} documents; 2026 is a partial year)")
    ax.set_ylim(0, 1)
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), fontsize=8, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(outdir / "fig1_topic_share_by_year.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig2_keyword_frequency(outdir, results_dir, min_words=300):
    df = pd.read_csv(results_dir / "keyword_frequency_by_year.csv")
    df = df[df["total_words"] >= min_words].sort_values("year")

    keyword_cols = [c for c in df.columns if c.endswith("_per_1000_words")]
    colors = ["#2C5FA8", "#2E7D45", "#B23B3B", "#B8860B", "#7B5EA7", "#3B8F9E"]

    fig, ax = plt.subplots(figsize=(8, 5))
    for col, color in zip(keyword_cols, colors):
        label = col.replace("_per_1000_words", "")
        ax.plot(df["year"], df[col], marker="o", markersize=3, linewidth=1.6, label=label, color=color)

    ax.set_xlabel("Publication year")
    ax.set_ylabel("Frequency per 1,000 words")
    ax.set_title(f"Keyword frequency trends by publication year\n"
                 f"(years with \u2265{min_words} words of text; 2026 is a partial year)")
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(outdir / "fig2_keyword_frequency_by_year.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig3_network(outdir, results_dir, top_n=60):
    edges = pd.read_csv(results_dir / "cooccurrence_edges_pmi.csv")
    comm = pd.read_csv(results_dir / "network_communities_pmi.csv")
    comm_map = dict(zip(comm["term"], comm["community"]))

    graph_full = nx.from_pandas_edgelist(edges, "term_a", "term_b", edge_attr="pmi")
    weighted_degree = dict(graph_full.degree(weight="pmi"))

    top_terms = sorted(weighted_degree, key=weighted_degree.get, reverse=True)[:top_n]
    graph = graph_full.subgraph(top_terms).copy()

    pos = nx.spring_layout(graph, seed=42, k=0.5, weight="pmi")
    node_colors = [COMMUNITY_COLORS.get(comm_map.get(n, -1), "#999999") for n in graph.nodes()]
    node_sizes = [200 + weighted_degree[n] * 15 for n in graph.nodes()]

    fig, ax = plt.subplots(figsize=(10, 9))
    nx.draw_networkx_edges(graph, pos, ax=ax, alpha=0.15, width=0.6, edge_color="#888888")
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=node_colors, node_size=node_sizes,
                            edgecolors="white", linewidths=0.6)
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=8, font_weight="normal")

    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=9, label=COMMUNITY_LABELS[k])
               for k, c in COMMUNITY_COLORS.items()]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.0, 1.0), fontsize=8, frameon=False,
              title="Louvain community", title_fontsize=9)

    full_density = graph_full.number_of_edges() / (graph_full.number_of_nodes() * (graph_full.number_of_nodes() - 1) / 2)
    ax.set_title(
        f"Co-occurrence network (top {top_n} terms by weighted degree, for visualization)\n"
        f"Full network: {graph_full.number_of_nodes()} nodes, {graph_full.number_of_edges()} edges, "
        f"density {full_density:.1%}",
        fontsize=10,
    )
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(outdir / "fig3_cooccurrence_network.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def fig4_model_selection(outdir, results_dir, selected_k=6):
    perplexity_df = pd.read_csv(results_dir / "model_selection_perplexity.csv")
    coherence_df = pd.read_csv(results_dir / "model_selection_coherence.csv")

    fig, ax1 = plt.subplots(figsize=(7.5, 5))

    color1 = "#B23B3B"
    ax1.plot(perplexity_df["k"], perplexity_df["perplexity"], marker="o", color=color1,
              linewidth=1.8, label="Held-out perplexity")
    ax1.set_xlabel("Number of topics (k)")
    ax1.set_ylabel("Held-out perplexity (lower = better fit)", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = "#2C5FA8"
    ax2.plot(coherence_df["k"], coherence_df["coherence_cv"], marker="s", color=color2,
              linewidth=1.8, label="Topic coherence (c_v)")
    ax2.set_ylabel("Topic coherence, c_v (higher = better interpretability)", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    ax1.axvline(selected_k, color="#555555", linestyle="--", linewidth=1, alpha=0.6)
    ax1.text(selected_k + 0.1, ax1.get_ylim()[1] * 0.95, f"k={selected_k}\n(retained)", fontsize=8, color="#333333")

    ax1.set_title(
        f"Model selection: candidate values of k\n"
        f"Both metrics technically favour k=3; k={selected_k} retained for thematic granularity "
        f"(see docs/topic-codebook.md)",
        fontsize=10,
    )
    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    fig.tight_layout()
    fig.savefig(outdir / "fig4_model_selection.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Generate manuscript figures from pipeline results.")
    parser.add_argument("--results-dir", default="results")
    parser.add_argument("--outdir", default="figures")
    parser.add_argument("--min-docs-per-year", type=int, default=5,
                         help="Minimum documents in a year for it to be plotted in fig1.")
    parser.add_argument("--min-words-per-year", type=int, default=300,
                         help="Minimum words of text in a year for it to be plotted in fig2.")
    parser.add_argument("--network-top-n", type=int, default=60,
                         help="Number of top-degree terms to include in the fig3 network visualization.")
    parser.add_argument("--selected-k", type=int, default=6)
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    fig1_topic_share(outdir, results_dir, min_docs=args.min_docs_per_year)
    print(f"Saved {outdir}/fig1_topic_share_by_year.png")

    fig2_keyword_frequency(outdir, results_dir, min_words=args.min_words_per_year)
    print(f"Saved {outdir}/fig2_keyword_frequency_by_year.png")

    fig3_network(outdir, results_dir, top_n=args.network_top_n)
    print(f"Saved {outdir}/fig3_cooccurrence_network.png")

    fig4_model_selection(outdir, results_dir, selected_k=args.selected_k)
    print(f"Saved {outdir}/fig4_model_selection.png")


if __name__ == "__main__":
    main()
