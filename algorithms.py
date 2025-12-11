import networkx as nx
from utils import is_transfer, find_all_nodes

# 환승 패널티 
TRANSFER_PENALTY = 10

def dijkstra(G, start, end):
    best_path = None
    best_cost = float("inf")

    for s in find_all_nodes(G, start):
        for e in find_all_nodes(G, end):
            try:
                def weight(u, v, data):
                    base = data["time"]
                    penalty = TRANSFER_PENALTY if is_transfer(u, v) else 0
                    return base + penalty

                path = nx.dijkstra_path(G, s, e, weight=weight)

                total_cost = sum(
                    G[path[i]][path[i+1]]["time"]
                    + (TRANSFER_PENALTY if is_transfer(path[i], path[i+1]) else 0)
                    for i in range(len(path)-1)
                )

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_path = path

            except:
                continue

    return best_path, best_cost
