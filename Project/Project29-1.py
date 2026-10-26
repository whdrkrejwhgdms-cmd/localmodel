from gtts import gTTS

def text_to_audio(text, output_file_path):
    # 언어 설정 (한국어 설정)
    language = 'ko'

    # gTTS 객체 생성
    tts = gTTS(text=text, lang=language, slow=False)

    # 오디오 파일로 저장
    tts.save(output_file_path)

if __name__ == "__main__":
    # 입력 텍스트
    input_text = "안녕하세요, 텍스트를 오디오 파일로 변환하는 예제입니다."

    # 출력 파일 경로
    output_file_path = "C:\\AutoCoder\\output_audio.mp3"

    # 텍스트를 오디오로 변환
    text_to_audio(input_text, output_file_path)

    print(f"텍스트가 오디오로 변환되었습니다. 경로는 {output_file_path} 입니다.")