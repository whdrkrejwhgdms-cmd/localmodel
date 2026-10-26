# 웹드라이버 매니저를 사용하여 Chrome 드라이버 설치 및 옵션 설정
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# ChromeOptions 객체를 생성합니다.
chrome_options = webdriver.ChromeOptions()
# ChromeDriver를 설치하고 Chrome 브라우저를 시작합니다.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

# Signal 뉴스 페이지(https://signal.bz/news)로 이동
driver.get(url='https://signal.bz/news')

# 페이지 로딩을 위해 5초 대기
time.sleep(5)

# 실시간 검색 순위 시간 정보 가져오기
ranktime = driver.find_element(By.XPATH,
'//*[@id="app"]/div/main/div/section/div/section/section[1]/div[1]/div[1]/span').text
print(ranktime)

# 실시간 검색 순위 요소 목록 가져오기
ranks = driver.find_elements(By.CLASS_NAME, 'rank-layer')

# 각 실시간 검색 순위 요소의 정보 추출 및 출력
for rank in ranks:
    # 순위 번호 추출
    num = rank.find_element(By.CLASS_NAME, 'rank-num').text
    # 검색어 추출
    search = rank.find_element(By.CLASS_NAME, 'rank-text').text
    # 순위 번호와 검색어 출력
    print(num + '. ' + search)

# 웹드라이버 종료
driver.quit()