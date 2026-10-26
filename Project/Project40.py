# 웹드라이버 매니저에서 Chrome 드라이버 설치
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Chrome 옵션 설정
chrome_options = webdriver.ChromeOptions()

# Chrome 드라이버 시작
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

# ppomppu 게시판 웹사이트 열기
driver.get(url='https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu')

# 페이지 로딩을 위한 암묵적인 대기 시간 설정
driver.implicitly_wait(time_to_wait=10)

# 게시판에서 타이틀과 링크를 추출할 요소 선택
items = driver.find_elements(By.CSS_SELECTOR,
'#revolution_main_table > tbody > tr > td:nth-child(3) > table > tbody > tr > td:nth-child(2) > div > a')

# 추출한 요소를 순회하며 타이틀과 링크 출력
for item in items:
    title = item.text
    site = item.get_attribute('href')
    print(title, site, sep='\t\t')