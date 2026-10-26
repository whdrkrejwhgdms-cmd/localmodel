import pandas as pd
import matplotlib.pyplot as plt

# 파일 읽기
df = pd.read_csv('C:\\AutoCoder\\log_count_results.csv', encoding='cp949')

# 로그 열에서 공백 이전 값 파싱
df['로그'] = df['로그'].str.split().str.get(0)

# 로그별 발생횟수 합산
result = df.groupby('로그')['발생횟수'].sum()

# 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'

# 막대 그래프 그리기
plt.bar(result.index, result.values, width=0.8)

# 수평축 레이블 각도 조정
plt.xticks(rotation=45, ha='right')

# 그래프 제목 설정
plt.title('로그별 발생횟수')

# 그래프 출력
plt.show()