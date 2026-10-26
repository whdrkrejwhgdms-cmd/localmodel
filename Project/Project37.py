from bs4 import BeautifulSoup
import requests

# 대상 URL 설정
URL = 'https://bbs.ruliweb.com/market/board/1020'

# 해당 URL에 대한 요청을 보내고, 응답을 받아 BeautifulSoup으로 파싱
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

# CSS 선택자를 사용하여 여러 태그를 포함하는 요소들을 선택
items = soup.select('#board_list > div > div.board_main.theme_default.theme_white > table > tbody > tr')

# 제목과 URL을 추출하고 출력
for item in items[7:]:
    # 각 항목을 선택자를 사용하여 추출하고, 필요한 정보를 변수에 할당
    id = item.select_one('td.id').text.strip()
    category = item.select_one('td.divsn').text.strip()
    subject = item.select_one('td.subject > div > a.deco').text.strip()
    writer = item.select_one('td.writer > a').text.strip()
    recommend = item.select_one('td.recomd').text.strip()
    hit = item.select_one('td.hit').text.strip()
    time = item.select_one('td.time').text.strip()

    # 추출한 정보를 출력
    print(id, category, subject, writer, recommend, hit, time, sep=',')