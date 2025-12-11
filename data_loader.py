import pandas as pd
import networkx as nx

def load_graph(base_path, trans_path):
    base = pd.read_csv(base_path)
    trans = pd.read_csv(trans_path)

    def time_to_min(t):
        mm, ss = t.split(":")
        return int(mm) + int(ss) / 60

    base["time_min"] = base["소요시간"].apply(time_to_min)

    trans["호선"] = trans["호선"].astype(str).str.replace("호선", "")
    trans["환승노선"] = trans["환승노선"].astype(str).str.replace("호선", "")
    trans["time_min"] = trans["환승소요시간"].apply(time_to_min)
    trans["distance_km"] = trans["환승거리"] / 1000

    G = nx.Graph()

    for line, group in base.groupby("호선"):
        group = group.sort_values("연번")
        for i in range(len(group) - 1):
            node1 = f"{group.iloc[i]['역명']}({line})"
            node2 = f"{group.iloc[i+1]['역명']}({line})"
            G.add_edge(node1, node2,
                       distance=group.iloc[i+1]["역간거리(km)"],
                       time=group.iloc[i+1]["time_min"],
                       type="move")

    for _, row in trans.iterrows():
        s = row["환승역명"]
        A = f"{s}({row['호선']})"
        B = f"{s}({row['환승노선']})"

        G.add_edge(A, B,
                   distance=row["distance_km"],
                   time=row["time_min"],
                   type="transfer")

    return G
