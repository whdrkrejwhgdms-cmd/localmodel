
import pandas as pd

# 1. CSV 파일 경로 지정
file_path = r"C:\이규영샘\소상공인시장진흥공단_상가(상권)정보_20260630\소상공인시장진흥공단_상가(상권)정보_서울_202606.csv"

# 2. 컬럼명만 읽기
df = pd.read_csv(
    file_path,
    encoding="utf-8-sig",
    nrows=0
)

# 3. 컬럼명 출력
print("=" * 50)
print("CSV 컬럼 목록")
print("=" * 50)

for number, column in enumerate(df.columns, start=1):
    print(f"{number}. {column}")

print("=" * 50)
print(f"전체 컬럼 개수: {len(df.columns)}")
