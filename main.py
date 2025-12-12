from data_loader import load_graph
from algorithms import dijkstra
from utils import station_exists, pretty
from visualizer import draw_path

# 그래프 로드
G = load_graph(
    "서울교통공사 역간거리 및 소요시간_240810.csv",
    "서울교통공사_환승역거리 소요시간 정보_20250331.csv"
)

while True:
    print("\n===== 서울 지하철 경로 탐색 시스템 =====")
    print("1. 최단 시간 경로")
    print("2. 붐비지 않는 경로(혼잡도 기반)")
    print("-1. 종료")

    mode_select = input("모드를 선택하세요: ").strip()
    if mode_select == "-1":
        break
    if mode_select not in ["1", "2"]:
        print("잘못된 선택!")
        continue

    mode = "normal" if mode_select == "1" else "low_congestion"  

    # 출발
    start = input("출발역 입력: ").strip()
    if start == "-1":
        print("\n프로그램을 종료합니다.")
        break

    if not station_exists(G, start):
        print(f"\n'{start}' 은(는) 존재하지 않는 역입니다. 다시 입력해주세요!\n")
        continue

    # 입력
    end = input("도착역 입력: ").strip()
    if end == "-1":
        print("\n프로그램을 종료합니다.")
        break

    if not station_exists(G, end):
        print(f"\n'{end}' 은(는) 존재하지 않는 역입니다. 다시 입력해주세요!\n")
        continue

    path, total_cost = dijkstra(G, start, end, mode=mode)

    if path is None:
        print("\n해당 역들 사이에 이동 가능한 경로가 없습니다.\n")
        continue

    # 실제 이동 시간 계산(패널티 제외)
    real_time = sum(G[path[i]][path[i+1]]["time"] for i in range(len(path)-1))

    print("\n=== ✅ 추천 경로 ===")   
    print(pretty(path))
    print(f"\n실제 이동 시간: {real_time:.2f}분")
    print(f"평가 비용(환승 패널티 포함): {total_cost:.2f}")

    draw_path(G, path, f"추천 경로: {start} → {end}")