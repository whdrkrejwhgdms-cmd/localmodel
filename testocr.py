import pytesseract
from PIL import Image

# Tesseract 실행 파일 경로
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 이미지 파일 경로
image_file = r"C:\이규영샘\캡처.PNG"

# 이미지에서 글자 추출
image = Image.open(image_file)
text = pytesseract.image_to_string(image, lang="kor")

# 결과 출력
print(text)