import speech_recognition as sr
import pyttsx3

# 마이크 인스턴스 생성
r = sr.Recognizer()

# 마이크에서 오디오를 녹음
with sr.Microphone() as source:
    print("말씀하세요.")
    audio = r.listen(source)

# 오디오를 인식
try:
    # 인식 결과를 출력
    text = r.recognize_google(audio, language='ko-KR')
    print(text)

    # 명령어 처리
    if "날씨" in text:
        weather = pyttsx3.speak("오늘은 맑은 날입니다. 기온은 20도입니다.")
    elif "시간" in text:
        time = pyttsx3.speak("지금은 12시입니다.")
    elif "뉴스" in text:
        news = pyttsx3.speak("오늘의 뉴스입니다.")
    else:
        # 모르는 명령어
        weather = pyttsx3.speak("죄송합니다. 무슨 말씀인지 모르겠습니다.")

except sr.UnknownValueError:
    print("음성을 인식할 수 없습니다.")

except sr.RequestError:
    print("알 수 없는 에러가 발생했습니다.")