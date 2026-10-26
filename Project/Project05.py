from googletrans import Translator

# googletrans 라이브러리에서 Translator 클래스를 가져와 translator 객체를 생성
translator = Translator()

# 영어 텍스트 파일의 경로와 번역된 한국어 텍스트를 저장할 파일의 경로를 변수에 할당
Read = "C:/AutoCoder/english.txt"
korean = "C:/AutoCoder/korean.txt"

# 영어 텍스트 파일을 읽어 lines 리스트에 저장
with open(Read, 'r') as f:
    lines = f.readlines()

# 각 라인을 번역하고, 번역된 텍스트를 새로운 파일에 저장하는 작업 수행
for line in lines:
    # line을 한국어로 번역
    translation = translator.translate(line, dest='ko')

    # 번역된 텍스트 출력
    print(translation.text)

    # 번역된 텍스트를 UTF8 인코딩으로 새로운 파일에 추가
    with open(korean, 'a', encoding='UTF8') as f:
        f.write(translation.text + '\n')