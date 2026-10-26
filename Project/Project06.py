import os
from datetime import datetime

# 작업 폴더 경로 설정
folder_path = "C:\\AutoCoder"

# 확장자가 .xlsx 또는 .docx 또는 .pptx 또는 .txt 인 파일을 찾아 리스트에 저장
found_list = [os.path.join(path, filename)
              for path, _, files in os.walk(folder_path)
              for filename in files if filename.endswith(('.xlsx', '.docx', '.pptx', '.txt'))]

# 현재 시간 기록
current_time = datetime.now()

# 찾은 파일에 대해 수정 시간 확인 및 최근 3일 이내에 수정된 파일 출력
for file_path in found_list:
    modification_time = os.path.getmtime(file_path)

    # 수정 시간을 YYYY-MM-DD 형식으로 출력
    formatted_time = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d')

    # 현재 시간에서 수정 시간을 뺀 시간 (소요 시간)
    elapsed_time = current_time - datetime.fromtimestamp(modification_time)

    # 소요 시간이 3일 이내 라면, 파일 경로와 수정 시각을 출력
    if elapsed_time.days <= 3:
        print('-'*100)
        print('파일 경로 :', file_path)
        print('수정 시각 : ', formatted_time)