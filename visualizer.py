import matplotlib.pyplot as plt
import networkx as nx
from utils import clean

def draw_path(G, path, title):
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(18, 15))
    nx.draw_networkx_nodes(G, pos, node_size=6, node_color="gray", alpha=0.15)
    nx.draw_networkx_edges(G, pos, width=0.3, edge_color="gray", alpha=0.15)

    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_size=200, node_color="blue")
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color="blue")

    nx.draw_networkx_labels(
        G, pos,
        font_size=4, 
        font_color="gray",
        font_family='Malgun Gothic',
    )
    nx.draw_networkx_labels(
        G, pos,
        labels={n: clean(n) for n in path},
        font_family='Malgun Gothic',
        font_size=12, font_color="black",
        bbox=dict(facecolor='white', edgecolor='blue', alpha=0.9)
    )

    plt.title(title, fontfamily='Malgun Gothic')
    plt.axis("off")
    plt.show()
