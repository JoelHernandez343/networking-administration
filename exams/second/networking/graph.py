import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.edges = []
        self.labels = {}

    def add_edge(self, a, b, label):
        self.edges.append((a, b))
        self.labels[(a, b)] = label

    def render(self):
        G = nx.Graph()
        G.add_edges_from(self.edges)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, labels={node: node for node in G.nodes()})
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=self.labels,
        )

        plt.savefig("./app/static/images/network.png", format="PNG")
        plt.clf()
        print("[Host] 'network.png' created")
        print("[Host] Done.")
