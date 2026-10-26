from os import listdir, makedirs
from os.path import isdir
from shutil import copyfile

# 스캔 경로 및 분류된 스캔 경로 정의
scanPath = "C:\\AutoCoder\\Scan"
classifiedPath = "C:\\AutoCoder\\ClassifiedScan"

# 스캔 경로의 파일 목록 조회
files = listdir(scanPath)

# 파일별로 처리
for file in files:
    # 파일명에서 필요한 부분 추출
    file_item = file[5:-4]
    file_item = file_item.split('_')

    # 연도, 월, 일 정보 추출
    year = file_item[0]
    month = file_item[1]
    day = file_item[2]

    # 새로운 디렉토리 경로 생성
    newDirectory = (classifiedPath +
                    "\\" + year +
                    "\\" + month +
                    "\\" + day)
    print('새로운 디렉토리 : ', newDirectory)

    # 디렉토리가 존재하지 않으면 생성
    if not isdir(newDirectory):
        makedirs(newDirectory)

    # 파일 복사
    sourceFile = scanPath + "\\" + file
    destinationFile = newDirectory + "\\" + file
    copyfile(sourceFile, destinationFile)