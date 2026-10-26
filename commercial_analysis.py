
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ==================================================
# 1. 기본 설정
# ==================================================

# CSV 파일 경로: 실제 파일 경로로 변경하세요.
file_path = Path(r"data\상권분석.csv")

# 결과 파일은 CSV 파일과 같은 폴더에 저장
output_folder = file_path.parent
excel_path = output_folder / "상권분석_결과.xlsx"

# 분석에 필요한 컬럼
columns = [
    "상가업소번호",
    "상호명",
    "시도명",
    "시군구명",
    "행정동명",
    "상권업종중분류명",
    "상권업종소분류명",
]

# 지역을 구분하는 기준
region_cols = ["시도명", "시군구명", "행정동명"]

# 상위 및 하위 지역 출력 개수
TOP_N = 10


# ==================================================
# 2. CSV 데이터 읽기
# ==================================================

print("=" * 60)
print("전국 상권분석 프로그램")
print("=" * 60)

if not file_path.exists():
    raise FileNotFoundError(
        f"CSV 파일을 찾을 수 없습니다: {file_path}"
    )

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

print(f"\n전체 데이터 행 수: {len(df):,}")
print(f"분석 대상 컬럼 수: {len(df.columns)}")


# ==================================================
# 3. 결측값 및 중복 데이터 확인
# ==================================================

# 데이터 정리 전 결측값 확인
missing_counts = df.isnull().sum()

# 중복 상가업소번호 확인
duplicate_count = df["상가업소번호"].duplicated().sum()

# 중복 데이터는 삭제하지 않음
quality_data = [
    ["전체 데이터 행 수", len(df)],
    ["전체 컬럼 수", len(df.columns)],
    ["결측값이 있는 셀 수", int(missing_counts.sum())],
    ["상가업소번호 결측 행 수",
     int(df["상가업소번호"].isnull().sum())],
    ["중복 상가업소번호 행 수", int(duplicate_count)],
]

quality_df = pd.DataFrame(
    quality_data,
    columns=["항목", "건수"]
)

missing_df = pd.DataFrame({
    "컬럼명": missing_counts.index,
    "결측값 수": missing_counts.values
})

print("\n[데이터 품질 확인]")
print(quality_df.to_string(index=False))

# 문자열 앞뒤 공백 제거
text_columns = [
    "상호명",
    "시도명",
    "시군구명",
    "행정동명",
    "상권업종중분류명",
    "상권업종소분류명",
]

for column in text_columns:
    df[column] = df[column].str.strip()

# 지역명과 업종명이 없는 데이터는 별도로 구분
for column in region_cols + [
    "상권업종중분류명",
    "상권업종소분류명"
]:
    df[column] = df[column].fillna("미분류")

# 상가업소번호가 없는 데이터도 분석에서 행 자체는 유지
df["상가업소번호"] = df["상가업소번호"].fillna("")

# 빈 문자열을 미입력으로 처리
df["상가업소번호"] = df["상가업소번호"].replace("", pd.NA)


# ==================================================
# 4. 지역별 전체 점포 현황
# ==================================================

region_total = (
    df.groupby(region_cols, dropna=False)
    .agg(
        데이터행수=("상호명", "size"),
        고유상가업소수=("상가업소번호", "nunique")
    )
    .reset_index()
)

region_total = region_total.sort_values(
    "고유상가업소수",
    ascending=False
)

print("\n[점포 수가 많은 행정동 상위 10개]")
print(
    region_total.head(TOP_N).to_string(index=False)
)


# ==================================================
# 5. 중분류 및 소분류 업종별 분석
# ==================================================

def analyze_industry(industry_column):
    """지역별 업종 점포 수와 업종 비중을 계산합니다."""

    result = (
        df.groupby(
            region_cols + [industry_column],
            dropna=False
        )
        .agg(
            데이터행수=("상호명", "size"),
            고유상가업소수=("상가업소번호", "nunique")
        )
        .reset_index()
    )

    # 해당 지역의 전체 점포 수 연결
    result = result.merge(
        region_total[
            region_cols + ["고유상가업소수"]
        ].rename(
            columns={"고유상가업소수": "지역전체고유점포수"}
        ),
        on=region_cols,
        how="left"
    )

    # 지역 내 해당 업종의 비중
    result["업종비중(%)"] = (
        result["고유상가업소수"]
        / result["지역전체고유점포수"].replace(0, pd.NA)
        * 100
    ).fillna(0).round(2)

    result = result.rename(
        columns={"고유상가업소수": "업종고유점포수"}
    )

    return result.sort_values(
        ["업종고유점포수", "업종비중(%)"],
        ascending=[False, False]
    )


middle_analysis = analyze_industry("상권업종중분류명")
small_analysis = analyze_industry("상권업종소분류명")


# ==================================================
# 6. 업종별 지역 상위 10개 및 하위 10개
# ==================================================

def make_rankings(data, industry_column):
    """업종마다 점포 수가 많은 지역과 적은 지역을 비교합니다."""

    ranking_data = []

    for industry, group in data.groupby(
        industry_column,
        sort=True
    ):
        # 해당 업종이 실제로 등록된 지역만 비교
        group = group.sort_values(
            ["업종고유점포수", "업종비중(%)"],
            ascending=[False, False]
        )

        top = group.head(TOP_N).copy()
        top.insert(0, "순위구분", "상위")

        bottom = group.sort_values(
            ["업종고유점포수", "업종비중(%)"],
            ascending=[True, True]
        ).head(TOP_N).copy()

        bottom.insert(0, "순위구분", "하위")

        ranking_data.extend([top, bottom])

    if ranking_data:
        return pd.concat(ranking_data, ignore_index=True)

    return pd.DataFrame()


middle_ranking = make_rankings(
    middle_analysis,
    "상권업종중분류명"
)

small_ranking = make_rankings(
    small_analysis,
    "상권업종소분류명"
)

print("\n[중분류 업종 분석 예시]")
print(middle_analysis.head(10).to_string(index=False))

print("\n[소분류 업종 분석 예시]")
print(small_analysis.head(10).to_string(index=False))


# ==================================================
# 7. 그래프 생성
# ==================================================

# Windows 한글 글꼴 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 그래프 1: 점포 수 상위 10개 행정동
top_regions = region_total.head(TOP_N).copy()

top_regions["지역명"] = (
    top_regions["시도명"] + " "
    + top_regions["시군구명"] + " "
    + top_regions["행정동명"]
)

top_regions = top_regions.sort_values("고유상가업소수")

plt.figure(figsize=(12, 7))
plt.barh(
    top_regions["지역명"],
    top_regions["고유상가업소수"]
)
plt.title("전국 점포 수 상위 10개 행정동")
plt.xlabel("고유 상가업소번호 수")
plt.ylabel("지역")
plt.tight_layout()
plt.savefig(
    output_folder / "지역별_점포수_상위10.png",
    dpi=150
)
plt.close()


# 그래프 2: 전국 소분류 업종별 점포 수 상위 10개
industry_total = (
    df.groupby("상권업종소분류명", dropna=False)
    .agg(
        고유상가업소수=("상가업소번호", "nunique")
    )
    .reset_index()
    .sort_values("고유상가업소수", ascending=False)
    .head(TOP_N)
    .sort_values("고유상가업소수")
)

plt.figure(figsize=(12, 7))
plt.barh(
    industry_total["상권업종소분류명"],
    industry_total["고유상가업소수"]
)
plt.title("전국 소분류 업종별 점포 수 상위 10개")
plt.xlabel("고유 상가업소번호 수")
plt.ylabel("업종")
plt.tight_layout()
plt.savefig(
    output_folder / "업종별_점포수_상위10.png",
    dpi=150
)
plt.close()


# ==================================================
# 8. Excel 보고서 저장
# ==================================================

with pd.ExcelWriter(
    excel_path,
    engine="openpyxl"
) as writer:

    quality_df.to_excel(
        writer, sheet_name="데이터품질", index=False
    )

    missing_df.to_excel(
        writer, sheet_name="컬럼별결측", index=False
    )

    region_total.to_excel(
        writer, sheet_name="지역별전체점포", index=False
    )

    middle_analysis.to_excel(
        writer, sheet_name="중분류업종분석", index=False
    )

    small_analysis.to_excel(
        writer, sheet_name="소분류업종분석", index=False
    )

    middle_ranking.to_excel(
        writer, sheet_name="중분류지역순위", index=False
    )

    small_ranking.to_excel(
        writer, sheet_name="소분류지역순위", index=False
    )

    industry_total.to_excel(
        writer, sheet_name="전국업종순위", index=False
    )


# ==================================================
# 9. 최종 결과
# ==================================================

print("\n" + "=" * 60)
print("상권분석 완료")
print("=" * 60)

print(f"Excel 보고서: {excel_path}")
print(f"지역별 그래프: {output_folder / '지역별_점포수_상위10.png'}")
print(f"업종별 그래프: {output_folder / '업종별_점포수_상위10.png'}")

print("\nExcel 파일에서 다음 시트를 확인하세요.")
print("1. 데이터품질")
print("2. 컬럼별결측")
print("3. 지역별전체점포")
print("4. 중분류업종분석")
print("5. 소분류업종분석")
print("6. 중분류지역순위")
print("7. 소분류지역순위")
print("8. 전국업종순위")
