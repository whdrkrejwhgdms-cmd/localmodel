import pandas as pd
import glob

# CSV 파일을 병합할 폴더 경로 지정
folder_path = 'C:/AutoCoder/'

# 해당 폴더에 있는 모든 CSV 파일의 경로 가져오기
file_list = glob.glob(folder_path + '*.csv')

# 각 CSV 파일을 데이터프레임으로 읽어와 리스트에 저장
dataframe_list = [pd.read_csv(file, encoding='cp949') for file in file_list]

# 데이터프레임을 하나로 병합
result_dataframe = pd.concat(dataframe_list, ignore_index=True)

# 병합된 데이터프레임을 새로운 CSV 파일로 저장
save_path = 'C:/AutoCoder/merged_file.csv'
result_dataframe.to_csv(save_path, index=False, encoding='cp949')

print(f'병합된 파일이 {save_path}에 저장되었습니다.!')