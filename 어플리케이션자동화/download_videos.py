"""Download the two requested YouTube videos using the yt-dlp command line."""

import shutil  # 실행 파일 검색 모듈: 아래에서 PATH에 등록된 yt-dlp 위치를 찾음
import subprocess  # 외부 프로그램 실행 모듈: 아래에서 yt-dlp로 각 URL을 다운로드함
import sys  # Python 실행 제어 모듈: 맨 아래에서 프로그램 종료 코드를 반환함


VIDEO_URLS = [
    "https://www.youtube.com/watch?v=DFjRjmSvHQ4",
    "https://www.youtube.com/watch?v=bnE-tUn-Mz8",
    "https://www.youtube.com/shorts/q82xDp7KVms"
]


def main():
    downloader = shutil.which("yt-dlp")  # shutil 사용 위치: yt-dlp 실행 파일 검색
    if downloader is None:
        print("yt-dlp를 찾을 수 없습니다. 먼저 yt-dlp를 설치하고 PATH에 추가하세요.")
        return 1

    for url in VIDEO_URLS:
        print("다운로드 중:", url)
        result = subprocess.run([downloader, url], check=False)  # subprocess 사용 위치: yt-dlp 실행
        if result.returncode != 0:
            print("다운로드 실패:", url)
            return result.returncode

    print("두 영상 다운로드가 완료되었습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # sys 사용 위치: main()의 성공/실패 코드를 운영체제에 전달
