from pathlib import Path

# 현재 파이썬 파일이 실행된 위치를 기준 폴더로 정합니다.
current_folder = Path.cwd()

# 찾은 모든 파일 경로를 저장할 빈 리스트를 만듭니다.
file_list = []

# 기준 폴더와 그 안의 모든 하위 폴더를 차례대로 살펴봅니다.
for path in current_folder.rglob("*.txt"):
    # 현재 항목이 파일인지 확인합니다. 폴더는 건너뜁니다.
    if path.is_file():
        # 파일의 전체 경로를 리스트에 추가합니다.
        file_list.append(str(path))

# 찾은 파일 경로를 출력합니다.
print(file_list)
