from data_loader import load_graph
from algorithms import compare_times
from visualizer import draw_performance

G = load_graph(
    "서울교통공사 역간거리 및 소요시간_240810.csv",
    "서울교통공사_환승역거리 소요시간 정보_20250331.csv"
)

print("\n=== 알고리즘 성능 비교 ===")
start = input("출발역 입력: ").strip()
end = input("도착역 입력: ").strip()

results = compare_times(G, start, end)   # 시간 측정
draw_performance(results, start, end)    # 그래프 시각화
