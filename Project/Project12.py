# yt_dlp 모듈을 임포트합니다.
import yt_dlp

# 다운로드 받고 싶은 유튜브 동영상의 URL들을 입력합니다.
urls = ("https://www.youtube.com/watch?v=JoTkhU2hFu8&t=7s",
        "https://www.youtube.com/watch?v=0LUrPUs6FNg&t=947s")

for url in urls:
    # YoutubeDL 객체를 생성합니다. outtmpl 옵션으로 다운로드 받을 위치와 파일명을 지정합니다.
    ydl = yt_dlp.YoutubeDL({"outtmpl": "C:/AutoCoder/%(title)s.%(ext)s"})

    # 동영상의 메타데이터를 딕셔너리 형태로 저장합니다.
    info_dict = ydl.extract_info(url, download=True)

    # 동영상이 다운로드 완료될 때까지 기다립니다.
    ydl.download([url])

    # 동영상의 제목과 파일 경로를 출력합니다.
    print("제목: ", info_dict["title"])
    print("재생시간(초): ", info_dict["duration"])