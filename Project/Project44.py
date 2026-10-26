# 셀레니움 및 관련 모듈 불러오기
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 크롬 옵션 설정 및 웹 드라이버 초기화
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

# 11번가 이동
driver.get('https://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain&xfrom=main^gnb')

# 스크롤 다운
SCROLL_PAUSE_SEC = 1

# 스크롤 높이 가져옴
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 끝까지 스크롤 다운
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # 1초 대기
    time.sleep(SCROLL_PAUSE_SEC)

    # 스크롤 다운 후 스크롤 높이 다시 가져옴
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

lists = driver.find_element(By.ID, 'bestPrdList').find_elements(By.CLASS_NAME, 'viewtype')

# 베스트 상품 목록 추출하기
for list in lists:
    bestlist = list.find_elements(By.TAG_NAME, 'li')
    for item in bestlist:
        print('-' * 100)
        print('NO: ' + item.find_element(By.CLASS_NAME, 'best').text)
        print('Product: ' + item.find_element(By.CLASS_NAME, 'pname').text)
        print('Price: ' + item.find_element(By.CLASS_NAME, 'sale_price').text)
        print('URL: ' + item.find_element(By.TAG_NAME,'a').get_attribute('href'))