import pandas as pd
import matplotlib.pyplot as plt

# 파일 읽기
df = pd.read_csv('C:\\AutoCoder\\log_count_results.csv', encoding='cp949')

# 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'

# x축, y축 레이블 폰트 크기 설정
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)

# 막대 그래프 그리기
plt.bar(df['로그'], df['발생횟수'], width=0.8)

# 수평축 레이블 각도 조정
plt.xticks(rotation=45, ha='right')

# 그래프 제목 설정
plt.title('로그별 발생횟수')

# 그래프 출력
plt.show()