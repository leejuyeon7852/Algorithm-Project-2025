import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ------------------------------------------
# 1) CSV 로드
# ------------------------------------------
base = pd.read_csv("서울교통공사 역간거리 및 소요시간_240810.csv")
trans = pd.read_csv("서울교통공사_환승역거리 소요시간 정보_20250331.csv")

def time_to_min(t):
    mm, ss = t.split(":")
    return int(mm) + int(ss) / 60

base["time_min"] = base["소요시간"].apply(time_to_min)

# 호선 이름 통일 
trans["호선"] = trans["호선"].astype(str).str.replace("호선", "")
trans["환승노선"] = trans["환승노선"].astype(str).str.replace("호선", "")

trans["time_min"] = trans["환승소요시간"].apply(time_to_min)
trans["distance_km"] = trans["환승거리"] / 1000

# ------------------------------------------
# 2) 그래프 생성 (노드 = 역명(호선))
# ------------------------------------------
G = nx.Graph()

for line, group in base.groupby("호선"):
    group = group.sort_values("연번")

    for i in range(len(group) - 1):
        node1 = f"{group.iloc[i]['역명']}({line})"
        node2 = f"{group.iloc[i+1]['역명']}({line})"

        dist = group.iloc[i+1]["역간거리(km)"]
        tmin = group.iloc[i+1]["time_min"]

        G.add_edge(node1, node2, distance=dist, time=tmin, type="move")

# ------------------------------------------
# 3) 환승 간선 추가
# ------------------------------------------
for _, row in trans.iterrows():
    s = row["환승역명"]
    lineA = row["호선"]
    lineB = row["환승노선"]

    nodeA = f"{s}({lineA})"
    nodeB = f"{s}({lineB})"

    # 환승 연결 추가
    G.add_edge(
        nodeA, nodeB,
        distance=row["distance_km"],
        time=row["time_min"],
        type="transfer"
    )

# ------------------------------------------
# 4) 여러 노드 찾기 (출발/도착 후보 모두 찾기)
# ------------------------------------------
def find_all_nodes(name):
    return [n for n in G.nodes() if n.startswith(f"{name}(")]

# ------------------------------------------
# 5) 최단경로 계산 (모든 후보 중 최소값 선택)
# ------------------------------------------
def find_best_path(graph, start_name, end_name, weight="time"):

    start_nodes = find_all_nodes(start_name)
    end_nodes = find_all_nodes(end_name)

    best_path = None
    best_cost = float("inf")

    for s in start_nodes:
        for e in end_nodes:
            try:
                path = nx.dijkstra_path(graph, s, e, weight=weight)
                cost = nx.dijkstra_path_length(graph, s, e, weight=weight)

                if cost < best_cost:
                    best_cost = cost
                    best_path = path

            except nx.NetworkXNoPath:
                continue

    return best_path, best_cost


# ------------------------------------------
# 6) 출력 포맷
# ------------------------------------------
def clean(n):
    return n.split("(")[0]

def line_of(n):
    return n.split("(")[1].replace(")", "")

def pretty(path):
    out = []
    for i in range(len(path)):
        out.append(f"{clean(path[i])}({line_of(path[i])})")

        if i < len(path) - 1 and clean(path[i]) == clean(path[i+1]):
            out.append(" ↳ [환승]")
    return "\n → ".join(out)

# ------------------------------------------
# 7) 사용자 입력 + 반복문 + 에러 처리 + 종료 옵션
# ------------------------------------------

def station_exists(name):
    """입력한 역 이름이 G의 노드 중 하나라도 포함하는지 체크"""
    for n in G.nodes():
        if n.startswith(f"{name}("):
            return True
    return False


while True:
    print("\n===== 서울 지하철 최단경로 조회 시스템 =====")
    print("종료하려면 -1 을 입력하세요.\n")

    # ---------------------------
    # 출발역 입력
    # ---------------------------
    start = input("출발역 입력: ").strip()
    if start == "-1":
        print("\n프로그램을 종료합니다.")
        break

    if not station_exists(start):
        print(f"\n⚠️ '{start}' 은(는) 존재하지 않는 역입니다. 다시 입력해주세요!\n")
        continue

    # ---------------------------
    # 도착역 입력
    # ---------------------------
    end = input("도착역 입력: ").strip()
    if end == "-1":
        print("\n프로그램을 종료합니다.")
        break

    if not station_exists(end):
        print(f"\n '{end}' 은(는) 존재하지 않는 역입니다. 다시 입력해주세요!\n")
        continue

    # ---------------------------
    # 최단경로 계산
    # ---------------------------
    path, total = find_best_path(G, start, end, weight="time")

    if path is None:
        print("\n 해당 역들 사이에 경로가 존재하지 않습니다.\n")
        continue

    print("\n=== ✅ 최단경로 (시간 기준) ===")
    print(pretty(path))
    #print(f"\n총 소요시간: {total:.2f} 분\n")

    # ---------------------------
    # 그래프 시각화
    # ---------------------------
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(18, 15))
    nx.draw_networkx_nodes(G, pos, node_size=6, node_color="gray", alpha=0.15)
    nx.draw_networkx_edges(G, pos, width=0.3, edge_color="gray", alpha=0.15)

    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_size=200, node_color="red")
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color="red")

    nx.draw_networkx_labels(
        G, pos,
        font_size=4,
        font_family='Malgun Gothic',
        font_color="gray",
        alpha=0.6
    )
    nx.draw_networkx_labels(
        G, pos,
        labels={n: clean(n) for n in path},
        font_family='Malgun Gothic',
        font_size=12,
        font_color="black",
        bbox=dict(facecolor='white', edgecolor='red', alpha=0.9)
    )

    plt.title(f"{start} → {end} 최단경로 (시간 기준, 환승 포함)")
    plt.axis("off")
    plt.show()