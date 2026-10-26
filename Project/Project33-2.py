from bs4 import BeautifulSoup
import requests

# 함수화 시키기
def financialData(page):
    res = requests.get(page)
    soup = BeautifulSoup(res.text, 'html.parser')

    body = soup.find('tbody')
    items = body.find_all('tr', {'onmouseover': 'mouseOver(this)'})

    # 데이터 전처리 (클렌징)
    for item in items:
        information = item.text
        info = information.split('\n')
        print([info[1], info[2], info[3], info[6].strip(), info[11].strip(),
               info[14], info[15], info[16], info[17], info[18]])

# 코스피
KSPAddress = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
for i in range(1, 44):
    financialData(KSPAddress + str(i))

# 코스닥
KSDAddress = 'https://finance.naver.com/sise/sise_market_sum.naver?sosok=1&page='
for i in range(1, 35):
    financialData(KSDAddress + str(i))