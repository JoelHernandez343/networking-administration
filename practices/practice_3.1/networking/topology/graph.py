import networkx as nx
from matplotlib import rcParams
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.edges = []
        self.labels = {}

    def add_edge(self, a, b, label):
        self.edges.append((a, b))
        self.labels[(a, b)] = label

    def render(self):
        plt.figure(figsize=(7, 7))
        rcParams.update({"figure.autolayout": True})

        G = nx.Graph()
        G.add_edges_from(self.edges)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, labels={node: node for node in G.nodes()}, with_labels=False)
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=self.labels,
        )

        for node, (x, y) in pos.items():
            plt.text(x, y, node, fontsize=10, ha="center", va="center")

        plt.savefig(
            "network.png",
            format="PNG",
            bbox_inches="tight",
        )
        plt.clf()
        print("[Host] 'network.png' created")
        print("[Host] Done.")
