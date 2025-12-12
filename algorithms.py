import networkx as nx
from utils import is_transfer, find_all_nodes
from congestion import get_congestion  
import time

# 환승 페널티
TRANSFER_PENALTY = 10

def heuristic(a, b):
    # edge distance 사용한 단순 휴리스틱
    # 실제로는 더 정교할 수 있지만 지금 그래프 구조에서는 충분함
    return 1  # 기본값 (네트워크 구조 때문에 너무 세게 주면 경로 꼬임)

def dijkstra(G, start, end, mode="normal"):  
    best_path = None
    best_cost = float("inf")

    for s in find_all_nodes(G, start):
        for e in find_all_nodes(G, end):
            try:

                def weight(u, v, data):
                    base = data["time"]
                    penalty = TRANSFER_PENALTY if is_transfer(u, v) else 0

                    # 혼잡도 기반 모드일 경우 혼잡도 weight 추가
                    if mode == "low_congestion":
                        cong_u = get_congestion(u)
                        cong_v = get_congestion(v)
                        congestion_weight = (cong_u + cong_v) / 2 * 0.2  # 혼잡도 가중치
                        return base + penalty + congestion_weight

                    # 기본 모드
                    return base + penalty

                path = nx.dijkstra_path(G, s, e, weight=weight)

                total_cost = sum(
                    weight(path[i], path[i+1], G[path[i]][path[i+1]])
                    for i in range(len(path) - 1)
                )

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_path = path

            except:
                continue

    return best_path, best_cost

def astar(G, start, end, mode="normal"):
    best_path = None
    best_cost = float("inf")

    for s in find_all_nodes(G, start):
        for e in find_all_nodes(G, end):
            try:

                def weight(u, v, data):
                    base = data["time"]
                    penalty = TRANSFER_PENALTY if is_transfer(u, v) else 0

                    if mode == "low_congestion":
                        cong_u = get_congestion(u)
                        cong_v = get_congestion(v)
                        congestion_weight = (cong_u + cong_v) / 2 * 0.2
                        return base + penalty + congestion_weight

                    return base + penalty

                # A* 경로 계산
                path = nx.astar_path(G, s, e, weight=weight,
                                     heuristic=lambda u, v: heuristic(u, v))

                # 비용 계산 
                total_cost = sum(
                    weight(path[i], path[i+1], G[path[i]][path[i+1]])
                    for i in range(len(path) - 1)
                )

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_path = path

            except Exception:
                continue

    return best_path, best_cost

# 시간 비교 
def compare_times(G, start, end): 
    results = {}

    # 다익스트라
    t0 = time.time()
    dijkstra(G, start, end)
    results["Dijkstra"] = time.time() - t0

    # A*
    t0 = time.time()
    astar(G, start, end)
    results["A*"] = time.time() - t0

    return results  