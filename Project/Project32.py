from bs4 import BeautifulSoup
import requests

# 날씨 쿼리
html = requests.get('https://search.naver.com/search.naver?query=강남+날씨')
soup = BeautifulSoup(html.text, 'html.parser')

# 위치
address = (soup.find('div', attrs={'class': 'title_area _area_panel'}).
           find('h2', attrs={'class', 'title'}).text)
print("위치 : " + address)

# 기본 날씨 정보 접근하기
weather_data = soup.find('div', {'class': 'weather_info'})

# 현재 온도
temperature = weather_data.find('div', attrs={'class': 'temperature_text'}).text.strip()[5:]
print("온도 : " + temperature)

# 날씨 상태
weatherStatus = weather_data.find('span', attrs={'class': 'weather before_slash'}).text
print("날씨 : " + weatherStatus)

# 공기 상태
air = soup.find('ul', attrs={'class': 'today_chart_list'})
infos = air.findAll('li', attrs={'class': 'item_today'})

# 공기 정보 가져오기 (미세먼지, 초미세먼지, 자외선, 일몰 등)
for info in infos:
    print(info.text.strip())