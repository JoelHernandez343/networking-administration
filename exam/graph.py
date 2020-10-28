import networkx as nx 
import matplotlib.pyplot as plt 

from networkx.drawing.nx_agraph import write_dot 

class Graph:
    def __init__(self):
        self.edges = []

    def add_edge(self, a, b):
        self.edges.append([a, b])

    def render(self):
        G = nx.Graph()
        G.add_edges_from(self.edges)
        nx.draw_networkx(G)
        
        write_dot(G, 'network.dot')
        print('[Host] \'network.dot\' created.')
        plt.savefig('network.png', format='PNG')
        print('[Host] \'network.png\' created')
        print('[Host] Render network...')
        plt.show()
        print ('[Host] Done.')
