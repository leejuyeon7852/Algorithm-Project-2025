import networkx as nx
from utils import is_transfer, find_all_nodes
from congestion import get_congestion  
import time
import math

# 환승 페널티
TRANSFER_PENALTY = 10

MAX_SPEED = 60

station_pos = None

def set_station_pos(pos):
    global station_pos
    station_pos = pos

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2

    return 2 * R * math.asin(math.sqrt(a))  # km

def pure_station(node):
    return node.split("(")[0]

def heuristic(a, b):
    if station_pos is None:
        return 0

    sa = pure_station(a)               
    sb = pure_station(b)              

    if sa not in station_pos or sb not in station_pos:
        return 0

    lat1, lon1 = station_pos[sa]
    lat2, lon2 = station_pos[sb]

    dist_km = haversine(lat1, lon1, lat2, lon2)

    # 거리 → 시간(분)
    return (dist_km / MAX_SPEED) * 60


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
                path = nx.astar_path(
                    G, s, e, 
                    weight=weight,
                    heuristic=lambda u, v: heuristic(u, v)
                )

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
def compare_times(G, start, end, repeat=20):
    results = {}

    # 다익스트라
    total = 0
    for _ in range(repeat):
        t0 = time.perf_counter()        
        dijkstra(G, start, end)
        total += time.perf_counter() - t0
    results["Dijkstra"] = total / repeat

    # A*
    total = 0
    for _ in range(repeat):
        t0 = time.perf_counter()        
        astar(G, start, end)
        total += time.perf_counter() - t0
    results["A*"] = total / repeat

    return results