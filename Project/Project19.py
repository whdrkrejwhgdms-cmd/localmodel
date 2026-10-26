from PIL import Image
import pytesseract

# 이미지 파일 경로 설정
image_path = "C:/AutoCoder/OCR_image.jpg"

# Tesseract OCR 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# 이미지에서 텍스트 추출
text = pytesseract.image_to_string(Image.open(image_path), lang="eng")

# 추출된 텍스트 출력
print(text)

# 추출된 텍스트를 텍스트 파일로 저장
with open("C:/AutoCoder/OCR_image.txt", "w", encoding="utf8") as f:
    f.write(text)