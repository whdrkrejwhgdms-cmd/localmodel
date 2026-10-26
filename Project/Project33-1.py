from bs4 import BeautifulSoup
import requests

financeKSPAddress = 'https://finance.naver.com/sise/sise_market_sum.naver?&page=1'
res = requests.get(financeKSPAddress)
soup = BeautifulSoup(res.text, 'html.parser')

body = soup.find('tbody')
items = body.find_all('tr', {'onmouseover': 'mouseOver(this)'})

# 첫 번째 항목만 출력
print(items[0].text.split('\n')[6].strip())