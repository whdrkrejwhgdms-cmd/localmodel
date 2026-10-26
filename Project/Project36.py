import requests
from bs4 import BeautifulSoup
import datetime

# 사용자로부터 키워드 입력 받기
keyword = input("키워드를 입력하세요 : ")

# 사람인 홈페이지에서 키워드를 이용해 채용 정보 검색
soup = requests.get(f'https://www.saramin.co.kr/'
                    f'zf_user/search?search&searchword={keyword}',
                    headers={'User-Agent': 'Mozilla/5.0'})
html = BeautifulSoup(soup.text, 'html.parser')
jobs = html.select('div.item_recruit')

# 검색 결과를 출력하는 루프
for job in jobs:
    try:
        # 현재 날짜를 'YYYY-MM-DD' 형식으로 가져오기
        today = datetime.datetime.now().strftime('%Y-%m-%d')

        # 채용 공고의 제목, 회사명, URL 등 필요한 정보 추출
        title = job.select_one('a')['title'].strip().replace(',', '')
        company = job.select_one('div.area_corp > strong > a').text.strip()
        url = 'https://www.saramin.co.kr' + job.select_one('a')['href']
        deadline = job.select_one('span.date').text.strip()
        location = job.select('div.job_condition > span')[0].text.strip()
        experience = job.select('div.job_condition > span')[1].text.strip()
        requirement = job.select('div.job_condition > span')[2].text.strip()
        jobtype = job.select('div.job_condition > span')[3].text.strip()

        # 결과 출력
        print(today, title, company, url, deadline, location, experience, jobtype)
    except Exception:
        pass