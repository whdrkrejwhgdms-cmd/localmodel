import os
from PIL import Image, ImageFont, ImageDraw

# 워터마크 글자 설정
text = "Copyright AutoCoder"
font = ImageFont.truetype("arial.ttf", 20)
color = (0, 0, 255)

# 워터마크 이미지 생성 함수
def create_watermark(image):
  watermark = Image.new("RGBA", image.size, (255, 255, 255, 0))
  draw = ImageDraw.Draw(watermark)
  draw.text((0, 0), text, font=font, fill=color)
  return watermark

# 이미지 파일 리스트 가져오기
image_list = os.listdir("C:\\AutoCoder")

# 이미지 파일마다 워터마크 삽입
for image_file in image_list:
  if image_file.endswith(".jpg") or image_file.endswith(".jpeg"):
    image = Image.open("C:\\AutoCoder\\{}".format(image_file))
    watermark = create_watermark(image)

    # Copyright 폴더가 없으면 생성
    if not os.path.exists("C:\\AutoCoder\\Copyright"):
      os.mkdir("C:\\AutoCoder\\Copyright")

    image.paste(watermark, (0, 0), mask=watermark)
    image.save("C:\\AutoCoder\\Copyright\\{}".format(image_file))