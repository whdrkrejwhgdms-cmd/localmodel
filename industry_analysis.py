
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# 1. 기본 설정
# ==========================================

file_path = Path(r"data\상권분석.csv")

output_folder = file_path.parent
excel_path = output_folder / "업종별_상권분석.xlsx"

columns = [
    "상가업소번호",
    "상호명",
    "시도명",
    "시군구명",
    "행정동명",
    "상권업종중분류명",
    "상권업종소분류명",
]

region_cols = ["시도명", "시군구명", "행정동명"]
TOP_N = 10


# ==========================================
# 2. CSV 읽기
# ==========================================

if not file_path.exists():
    raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

try:
    df = pd.read_csv(
        file_path,
        usecols=columns,
        dtype={"상가업소번호": "string"},
        encoding="utf-8-sig"
    )
except UnicodeDecodeError:
    df = pd.read_csv(
        file_path,
        usecols=columns,
        dtype={"상가업소번호": "string"},
        encoding="cp949"
    )

print(f"전체 데이터 행 수: {len(df):,}")


# ==========================================
# 3. 데이터 정리
# ==========================================

text_cols = [
    "상호명",
    "시도명",
    "시군구명",
    "행정동명",
    "상권업종중분류명",
    "상권업종소분류명",
]

for col in text_cols:
    df[col] = df[col].str.strip()

# 지역 정보가 없는 경우
for col in region_cols:
    df[col] = df[col].fillna("미분류")

# 업종명이 없는 행은 업종 검색에서 제외
df["상가업소번호"] = df["상가업소번호"].replace("", pd.NA)

# 데이터 품질 확인
print("\n[데이터 확인]")
print("상가업소번호 결측:", df["상가업소번호"].isna().sum())
print("중복 상가업소번호 행:", df["상가업소번호"].duplicated().sum())


# ==========================================
# 4. 업종 입력 및 검색
# ==========================================

print("\n업종 분류를 선택하세요.")
print("1. 중분류")
print("2. 소분류")

choice = input("선택 (1 또는 2): ").strip()

if choice == "1":
    industry_col = "상권업종중분류명"
elif choice == "2":
    industry_col = "상권업종소분류명"
else:
    raise ValueError("1 또는 2를 입력하세요.")

keyword = input("분석할 업종명: ").strip()

if not keyword:
    raise ValueError("업종명을 입력하세요.")

# 입력한 단어가 포함된 업종 검색
matched = df[
    df[industry_col].str.contains(
        keyword,
        case=False,
        na=False,
        regex=False
    )
].copy()

if matched.empty:
    print(f"'{keyword}'에 해당하는 업종이 없습니다.")
    print("\n등록된 업종명 예시:")
    print(
        df[industry_col]
        .dropna()
        .drop_duplicates()
        .sort_values()
        .head(50)
        .to_string(index=False)
    )
    raise SystemExit

print("\n검색된 업종:")
print(matched[industry_col].value_counts().to_string())
print(f"\n검색된 데이터 행 수: {len(matched):,}")


# ==========================================
# 5. 지역별 전체 점포 수 계산
# ==========================================

# 고유 상가업소번호 수를 점포 수로 사용합니다.
# 식별번호가 없는 행은 고유 점포 수에 포함하지 않습니다.
region_total = (
    df.groupby(region_cols, dropna=False)
    .agg(
        전체데이터행수=("상가업소번호", "size"),
        전체고유점포수=("상가업소번호", "nunique")
    )
    .reset_index()
)


# ==========================================
# 6. 지역별 업종 점포 수 계산
# ==========================================

industry_region = (
    matched.groupby(region_cols, dropna=False)
    .agg(
        업종데이터행수=("상가업소번호", "size"),
        업종고유점포수=("상가업소번호", "nunique")
    )
    .reset_index()
)

# 지역별 전체 점포 수와 업종 점포 수 결합
result = industry_region.merge(
    region_total,
    on=region_cols,
    how="left"
)


# ==========================================
# 7. 지역 내 업종 비중 계산
# ==========================================

# 계산식:
# 업종 비중(%) = 업종 고유 점포 수 / 지역 전체 고유 점포 수 * 100

result["업종비중(%)"] = (
    result["업종고유점포수"]
    .div(result["전체고유점포수"].replace(0, pd.NA))
    .mul(100)
).fillna(0).round(2)

# 지역명 결합
result["지역명"] = (
    result["시도명"] + " "
    + result["시군구명"] + " "
    + result["행정동명"]
)

# 업종 점포 수가 많은 순서로 정렬
result = result.sort_values(
    ["업종고유점포수", "업종비중(%)"],
    ascending=[False, False]
)

display_cols = [
    "지역명",
    "전체고유점포수",
    "업종고유점포수",
    "업종비중(%)",
]

print("\n" + "=" * 70)
print(f"'{keyword}' 지역별 업종 분석")
print("=" * 70)

print("\n[지역별 업종 비중 상위 10개]")
print(
    result.sort_values(
        "업종비중(%)", ascending=False
    )[display_cols].head(TOP_N).to_string(index=False)
)

print("\n[업종 점포 수 상위 10개]")
print(result[display_cols].head(TOP_N).to_string(index=False))


# ==========================================
# 8. 업종 점포 수 상위·하위 지역
# ==========================================

top_regions = result.head(TOP_N).copy()

bottom_regions = (
    result.sort_values(
        ["업종고유점포수", "업종비중(%)"],
        ascending=[True, True]
    )
    .head(TOP_N)
    .copy()
)

print("\n[업종 점포 수 하위 10개]")
print(bottom_regions[display_cols].to_string(index=False))


# ==========================================
# 9. 그래프 설정
# ==========================================

# Windows 한글 글꼴
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


# 그래프 1: 업종 점포 수 상위 10개 지역
plot_top = top_regions.sort_values("업종고유점포수")

plt.figure(figsize=(12, 7))
plt.barh(
    plot_top["지역명"],
    plot_top["업종고유점포수"]
)
plt.title(f"'{keyword}' 업종 점포 수 상위 10개 지역")
plt.xlabel("고유 점포 수")
plt.ylabel("지역")
plt.tight_layout()
plt.savefig(
    output_folder / "업종_점포수_상위10.png",
    dpi=150
)
plt.show()


# 그래프 2: 업종 점포 수 하위 10개 지역
plot_bottom = bottom_regions.sort_values("업종고유점포수")

plt.figure(figsize=(12, 7))
plt.barh(
    plot_bottom["지역명"],
    plot_bottom["업종고유점포수"]
)
plt.title(f"'{keyword}' 업종 점포 수 하위 10개 지역")
plt.xlabel("고유 점포 수")
plt.ylabel("지역")
plt.tight_layout()
plt.savefig(
    output_folder / "업종_점포수_하위10.png",
    dpi=150
)
plt.show()


# 그래프 3: 지역 내 업종 비중 상위 10개 지역
share_top = (
    result.sort_values("업종비중(%)", ascending=False)
    .head(TOP_N)
    .sort_values("업종비중(%)")
)

plt.figure(figsize=(12, 7))
plt.barh(
    share_top["지역명"],
    share_top["업종비중(%)"]
)
plt.title(f"'{keyword}' 지역 내 업종 비중 상위 10개")
plt.xlabel("지역 전체 점포 중 해당 업종 비중 (%)")
plt.ylabel("지역")
plt.tight_layout()
plt.savefig(
    output_folder / "업종비중_상위10.png",
    dpi=150
)
plt.show()


# ==========================================
# 10. Excel 보고서 저장
# ==========================================

with pd.ExcelWriter(
    excel_path,
    engine="openpyxl"
) as writer:

    # 검색된 원본 행
    matched.to_excel(
        writer,
        sheet_name="검색업종데이터",
        index=False
    )

    # 전체 지역별 업종 분석 결과
    result.to_excel(
        writer,
        sheet_name="지역별업종분석",
        index=False
    )

    # 점포 수 상위·하위
    top_regions.to_excel(
        writer,
        sheet_name="점포수상위10",
        index=False
    )

    bottom_regions.to_excel(
        writer,
        sheet_name="점포수하위10",
        index=False
    )

    # 업종 비중 상위 지역
    share_top.to_excel(
        writer,
        sheet_name="업종비중상위10",
        index=False
    )

    # 지역별 전체 점포 수
    region_total.to_excel(
        writer,
        sheet_name="지역별전체점포",
        index=False
    )


# ==========================================
# 11. 완료 메시지
# ==========================================

print("\n" + "=" * 70)
print("분석이 완료되었습니다.")
print("=" * 70)

print(f"Excel 보고서: {excel_path}")
print("그래프 파일:")
print(output_folder / "업종_점포수_상위10.png")
print(output_folder / "업종_점포수_하위10.png")
print(output_folder / "업종비중_상위10.png")
