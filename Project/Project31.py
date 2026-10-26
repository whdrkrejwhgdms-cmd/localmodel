import requests
from pandas import DataFrame
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os

# 현재 날짜 및 시간 정보 가져오기
date = datetime.now().strftime('%Y_%m_%d')

# 검색어 및 뉴스 기사 수 입력 받기
query = input('검색어를 입력하세요: ')
news_num = int(input('뉴스 기사의 총 수를 입력하세요 (숫자만 입력): '))
query_param = query.replace(' ', '+')
print(query_param)

# 네이버 뉴스 검색 URL 설정
news_url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={query_param}'
print(news_url)

# 첫 페이지 크롤링
req = requests.get(news_url)
soup = BeautifulSoup(req.text, 'html.parser')

# 크롤링 결과를 저장할 딕셔너리 및 인덱스 초기화
news_dict = {}
idx = 1
cur_page = 1

print()
print(f'네이버 뉴스 {query} 크롤링 중...')

# 뉴스 기사 수가 목표에 도달할 때까지 반복
while idx <= news_num:
    table = soup.find('ul', {'class': 'list_news'})
    li_list = table.find_all('li', {'id': re.compile('sp_nws.*')})
    area_list = [li.find('div', {'class': 'news_area'}) for li in li_list]
    a_list = [area.find('a', {'class': 'news_tit'}) for area in area_list]

    # 현재 페이지의 기사 중 목표 수만큼 저장
    for n in a_list[:min(len(a_list), news_num - idx + 1)]:
        news_dict[idx] = {'Headline': n.get('title'),
                          'URL': n.get('href')}
        idx += 1

    # 다음 페이지로 이동
    cur_page += 1
    pages = soup.find('div', {'class': 'sc_page_inner'})
    next_page_url = [p for p in pages.find_all('a') if p.text == str(cur_page)][0].get('href')
    req = requests.get('https://search.naver.com/search.naver' + next_page_url)
    soup = BeautifulSoup(req.text, 'html.parser')

print(f'네이버 뉴스 {query} 크롤링 완료')
news_df = DataFrame(news_dict).T

# 엑셀 파일 저장
folder_path = "C:\\AutoCoder"
xlsx_file_name = f'Naver News_{query}_{date}.xlsx'
news_df.to_excel(f'{folder_path}\\{xlsx_file_name}', index_label='No.')

print(f'Excel 저장 완료 | 경로: {folder_path}\\{xlsx_file_name}')
os.startfile(folder_path)