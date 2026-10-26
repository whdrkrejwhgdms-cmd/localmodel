import os
from PIL import Image

# 타겟 폴더 지정
target_dir = "C:/AutoCoder"

# os.walk를 통해 시작 디렉토리부터 하위 디렉토리, 경로, 파일들 정보 가져오기
for (root, dirs, files) in os.walk(target_dir):
    # 이미지 파일만 처리
    for file in files:
        if file.endswith((".jpg", ".png", ".jpeg", ".bmp")):
            # 이미지 파일 열기
            image = Image.open(os.path.join(root, file))

            # 이미지 사이즈를 절반으로 줄임
            image = image.resize((int(image.size[0] * 0.6), int(image.size[1] * 0.4)))

            # 이미지 저장
            if not os.path.exists(os.path.join(root, "resize")):
                os.mkdir(os.path.join(root, "resize"))
            image.save(os.path.join(root, "resize", file))