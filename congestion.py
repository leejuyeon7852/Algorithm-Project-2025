import pandas as pd
from datetime import datetime

# CSV 로드
df = pd.read_csv("서울교통공사_지하철혼잡도정보_20250930.csv")

# 현재 시간 → 가장 가까운 컬럼으로 변환
def current_time_column():
    now = datetime.now()
    h = now.hour
    m = now.minute

    # 예: 8:12 → "8시00분"
    if m < 30:
        col = f"{h:02d}시00분"
    else:
        col = f"{h:02d}시30분"
    return col

# 역이름(역명), 호선 파싱
def parse_node(node):
    name = node.split("(")[0]
    line = node.split("(")[1].replace(")", "")
    return name, line

# 혼잡도 가져오기
def get_congestion(node):
    name, line = parse_node(node)
    col = current_time_column()

    row = df[(df["출발역"] == name) & (df["호선"] == f"{line}호선")]
    if row.empty:
        return 0.0

    try:
        return float(row[col].values[0])
    except:
        return 0.0
