import pandas as pd

# 병합된 CSV 파일 읽기
file_path = 'C:/AutoCoder/merged_file.csv'
data_frame = pd.read_csv(file_path, encoding='cp949')

# '로그' 열에서 각 유형의 발생 횟수 계산
log_count = data_frame['로그'].value_counts().reset_index()

# 결과를 새로운 CSV 파일로 저장
log_count_file_path = 'C:/AutoCoder/log_count_results.csv'
log_count.to_csv(log_count_file_path,
                 header=['로그', '발생횟수'],
                 index=False,
                 encoding='cp949')

print(f'로그 카운트 결과가 {log_count_file_path}에 저장되었습니다.')