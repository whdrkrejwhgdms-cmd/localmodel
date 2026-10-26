# 필요한 라이브러리 가져오기
import requests
from bs4 import BeautifulSoup

# 검색 키워드 입력 받기
keyword = input("검색 키워드를 입력하세요: ")

# 웹 페이지에서 데이터 수집
soup = requests.get(f'https://www.jobkorea.co.kr/Search/?stext={keyword}',
                    headers={'User-Agent': 'Mozilla/5.0'})
html = BeautifulSoup(soup.text, 'html.parser').select_one('div.list-default')
jobs = html.select('li.list-post')

# 채용 정보를 반복하면서 데이터 추출
for job in jobs:
    company = job.select_one('a.name').text
    description = job.select_one('a.title').text.strip()
    url = 'https://www.jobkorea.co.kr/' + job.find('a')['href']
    location = job.select_one('span.loc').text.strip()
    apply = job.select_one('div.post-list-apply').text.strip()

    # 채용 정보 출력
    print(company, description, url, location, apply)