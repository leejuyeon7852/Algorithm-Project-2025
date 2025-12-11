from turtle import distance
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import networkx as nx

# csv 불러오기
df = pd.read_csv("서울교통공사 역간거리 및 소요시간_240810.csv")

# 시간 문자열 -> 분 단위로 변환 함수
def time_to_minutes(t):
    mm, ss = t.split(":")
    return int(mm) + int(ss) / 60

df["time_min"] = df["소요시간"].apply(time_to_minutes)

# 그래프 생성
G = nx.Graph()

# 호선별 정렬 후, 이웃역끼리 edge 생성
for line, group in df.groupby("호선"):
    group = group.sort_values("연번")

    for i in range(len(group)-1):
        s1 = group.iloc[i]["역명"]
        s2 = group.iloc[i + 1]["역명"]
        dist = group.iloc[i + 1]["역간거리(km)"]
        tmin = group.iloc[i + 1]["time_min"]

        # 거리, 시간 저장
        G.add_edge(s1, s2, distance=dist, time=tmin)

# 다익스트라 최단경로
def shortest_path(graph, start, end, weight_type="distance"):
    path = nx.dijkstra_path(graph, start, end, weight=weight_type)
    total = nx.dijkstra_path_length(graph, start, end, weight=weight_type)
    return path, total

# 테스트
start = "강남"
end = "시청"

path, total = shortest_path(G, start, end, weight_type="distance")

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(14, 12))

pos = nx.spring_layout(G, seed=42)  # 레이아웃 동일하게 유지

# 전체 그래프 
nx.draw_networkx_nodes(G, pos, node_size=10, node_color="lightgray", alpha=0.2)
nx.draw_networkx_edges(G, pos, width=0.3, edge_color="gray", alpha=0.2)

nx.draw_networkx_labels(
    G, pos,
    font_size=5,                  
    font_family='Malgun Gothic',
    font_color="gray",
    bbox=dict(facecolor='white', edgecolor='none', alpha=0.4)
)

# 최단경로 강조 
path_edges = list(zip(path, path[1:]))

nx.draw_networkx_nodes(G, pos, nodelist=path, node_size=200, node_color="red")
nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color="red")

labels = {node: node for node in path}
nx.draw_networkx_labels(
    G, pos, labels=labels,
    font_size=10,
    font_family='Malgun Gothic',
    font_color="black",
    bbox=dict(facecolor='white', edgecolor='red', boxstyle="round,pad=0.2", alpha=0.9)
)

plt.title(f"{start} → {end} 최단경로 (거리 기준)", fontsize=16)
plt.axis("off")
plt.show()