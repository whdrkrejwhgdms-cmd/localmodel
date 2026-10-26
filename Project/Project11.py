import shutil
import os

# 원본 디렉토리와 대상 디렉토리 지정
source_folder = r"C:\AutoCoder\Source"
target_folder = r"C:\AutoCoder\Destination"

# 대상 디렉토리가 이미 존재하는지 확인하고 없으면 생성
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 원본 디렉토리의 내용을 대상 디렉토리로 복사
for item in os.listdir(source_folder):
    source_item = os.path.join(source_folder, item)
    target_item = os.path.join(target_folder, item)

    # 파일이 이미 존재하면 건너뛰기
    if os.path.exists(target_item):
        print(f"{target_item} 이미 존재하므로 건너뜁니다.")
        continue

    # 파일이 아니라면 폴더를 생성하고 내용 복사
    if os.path.isdir(source_item):
        shutil.copytree(source_item, target_item)
    else:
        shutil.copy2(source_item, target_item)
        print(f"{source_item} 파일을 {target_item}로 복사하였습니다.")

# 전체 백업이 종료되고 안내문 출력
print('-'*100)
print(f"{source_folder}의 내용이 {target_folder}로 전체 복사가 완료되었습니다.")