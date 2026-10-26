# yt_dlp 라이브러리를 가져옵니다.
import yt_dlp

# 유튜브 채널 URL 설정
channel_url = "https://www.youtube.com/@joo_pd/shorts"

# 동영상 다운로드 경로 설정
output_path = "C:\\AutoCoder\\%(title)s.%(ext)s"

# yt_dlp 인스턴스 생성, 다운로드 경로 설정
extractor = yt_dlp.YoutubeDL({"outtmpl": output_path})

# 채널 정보 추출 및 동영상 다운로드
extractor.extract_info(channel_url, download=True)