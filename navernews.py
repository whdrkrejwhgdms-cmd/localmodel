import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# 1. 네이버 뉴스 접속
url = "https://news.naver.com/section/101"
response = requests.get(url)

# 2. HTML 분석
soup = BeautifulSoup(response.text, "html.parser")

# 3. 뉴스 제목 추출
headlines = soup.select(".sa_text_title")

# 4. 엑셀 파일 생성
wb = Workbook()
ws = wb.active
ws.title = "뉴스 헤드라인"

# 제목 행 작성
ws.append(["번호", "뉴스 제목"])

# 뉴스 제목 저장
for i, headline in enumerate(headlines, 1):
    title = headline.get_text(strip=True)
    ws.append([i, title])

# 엑셀 파일 저장
wb.save("naver_news.xlsx")

print("엑셀 저장 완료: naver_news.xlsx")