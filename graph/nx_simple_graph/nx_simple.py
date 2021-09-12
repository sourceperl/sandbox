#!/usr/bin/env python3

# simple use of networkx to draw a directed graph

import networkx as nx
import matplotlib.pyplot as plt

# design a digraph network
G = nx.DiGraph()
G.add_edge(1, 2, weight=1)
G.add_edge(1, 3, weight=1)
G.add_edge(1, 5, weight=1)
G.add_edge(2, 3, weight=1)
G.add_edge(3, 4, weight=2)
G.add_edge(4, 5, weight=2)

# nodes position
pos = {1: (0, 0), 2: (-1, 0.3), 3: (2, 0.17), 4: (4, 0.255), 5: (5, 0.03)}

# draw nodes at fixed positions (with options)
options = {
    'font_size': 36,
    'font_color': 'white',
    'node_size': 3000,
    'node_color': 'orange',
    'edgecolors': 'black',
    'linewidths': 5,
    'width': 5,
}
nx.draw_networkx(G, pos, **options)

# add weight as edge label on the drawing
labels_d = nx.get_edge_attributes(G, 'weight')
labels_d[(1, 5)] = 'an override label (edge 1 > 5)'
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_d)

# show
plt.axis('off')
plt.show()
