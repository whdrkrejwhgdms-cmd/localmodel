import requests
from bs4 import BeautifulSoup
import pandas as pd

# YES24 기본 페이지 접속하여 html 기본파서로 파싱 준비 완료
url = 'http://www.yes24.com/Main/default.aspx'
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

# 베스트셀러가 있는 li 태그 안에 클래스명이 tp02로 접근
books = soup.select('li.tp02')

# 데이터프레임에 넣을 리스트 초기화
book_list = []

# 각각의 태그에 접근하여 순위, 제목, 저자, URL 정보 추출
for book in books:
    rank = book.select('strong')[0].text
    title = book.select('strong')[1].text
    author = book.select('em')[1].text
    url = 'http://www.yes24.com' + book.select_one('a')['href']
    book_list.append([rank, title, author, url])

# Pandas를 이용하여 데이터프레임 생성 후 엑셀로 저장하기
df = pd.DataFrame(book_list, columns=['순위', '제목', '저자', '링크'])
df.to_excel('C:/AutoCoder/yes24_bestTop10.xlsx', index=False)