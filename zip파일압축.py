import os
import zipfile


# 1. 압축할 폴더 경로 입력
source_folder = input("압축할 폴더 경로를 입력하세요: ")

# 2. 폴더 경로 확인
if not os.path.isdir(source_folder):
    print("오류: 존재하지 않는 폴더입니다.")

else:
    # 3. ZIP 파일 저장 경로 입력
    zip_path = input("저장할 ZIP 파일 경로를 입력하세요: ")

    # ZIP 확장자가 없으면 추가
    if not zip_path.lower().endswith(".zip"):
        zip_path += ".zip"

    # 4. 기존 ZIP 파일 확인
    if os.path.exists(zip_path):
        answer = input("파일이 이미 있습니다. 덮어쓸까요? (y/n): ")

        if answer.lower() != "y":
            print("압축을 취소했습니다.")
            exit()

    try:
        # 5. ZIP 파일 생성
        with zipfile.ZipFile(
            zip_path,
            "w",
            compression=zipfile.ZIP_DEFLATED
        ) as zip_file:

            # 6. 폴더와 하위 폴더의 파일 검색
            for folder, subfolders, files in os.walk(source_folder):

                for file in files:
                    # 원본 파일의 전체 경로
                    file_path = os.path.join(folder, file)

                    # ZIP 내부에 저장할 상대 경로
                    arcname = os.path.relpath(
                        file_path, source_folder
                    )

                    # 7. ZIP 파일에 추가
                    zip_file.write(file_path, arcname)

        print("압축이 완료되었습니다!")
        print("저장 위치:", os.path.abspath(zip_path))

    except (OSError, zipfile.LargeZipFile) as e:
        print("압축 중 오류가 발생했습니다:", e)