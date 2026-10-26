from gtts import gTTS

def text_file_to_audio(input_file_path, output_file_path):
    # 텍스트 파일에서 내용 읽기
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # 언어 설정 (영어)
    language = 'en'

    # gTTS 객체 생성
    tts = gTTS(text=text_content, lang=language, slow=False)

    # 오디오 파일로 저장
    tts.save(output_file_path)

if __name__ == "__main__":
    # 입력 텍스트 파일 경로
    input_file_path = "C:\\AutoCoder\\english_input.txt"

    # 출력 파일 경로
    output_file_path = "C:\\AutoCoder\\english_output_audio.mp3"

    # 텍스트 파일 내용인 영어를 음성파일로 변환
    text_file_to_audio(input_file_path, output_file_path)

    print(f"텍스트 파일 내용이 오디오로 변환되었습니다. 경로 : {output_file_path}")