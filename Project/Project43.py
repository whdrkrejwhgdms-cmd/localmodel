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

# G마켓의 베스트 상품 페이지로 이동
driver.get("https://www.gmarket.co.kr/n/best")
time.sleep(5)

# 베스트 상품 목록 찾기
lists = driver.find_element(By.CLASS_NAME, 'best-list')
lis = lists.find_elements(By.TAG_NAME, 'li')

# 각 상품에 대한 정보 출력
for li in lis:
    rank = li.find_element(By.TAG_NAME, 'p').text
    item = li.find_element(By.CLASS_NAME, 'itemname').text
    price = li.find_element(By.CLASS_NAME, 's-price').text.split('\n')[1]
    itemURL = li.find_element(By.TAG_NAME, 'a').get_attribute('href')
    print('-' * 100)
    print(f'제품 순위 : {rank}')
    print(f'제품 명 : {item}')
    print(f'가격 : {price}')
    print(f'사이트 주소 : {itemURL}')