import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# 크롬 드라이버를 설정합니다.
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

# Jobplanet 사이트에 접속하여 회사 리뷰 페이지를 엽니다.
driver.get('https://www.jobplanet.co.kr/companies/30139/reviews/삼성전자')

# 회사명을 찾아 출력합니다.
company = driver.find_element(By.CLASS_NAME, 'name').text
print('='*100)
print('회사 : ' + company)
print('='*100)
time.sleep(5)

# 전체 평점을 찾아 출력합니다.
ratePoint = driver.find_element(By.XPATH,
'//*[@id="premiumReviewStatistics"]/div/div[1]/div/div[2]/div[1]/div/span').text
print('전체 평점 : ' + ratePoint)

# 복지 및 급여 평점을 찾아 출력합니다.
wellfarePoint = driver.find_element(By.XPATH,
'//*[@id="premiumReviewStatistics"]/div/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/span[2]').text
print('* 복지 및 급여 : ' + wellfarePoint)

# 업무와 삶의 균형 평점을 찾아 출력합니다.
workandlife = driver.find_element(By.XPATH,
'//*[@id="premiumReviewStatistics"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/span[2]').text
print('* 업무와 삶의 균형 : ' + workandlife)

# 사내문화 평점을 찾아 출력합니다.
culture = driver.find_element(By.XPATH,
'//*[@id="premiumReviewStatistics"]/div/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/span[2]').text
print('* 사내문화 : ' + culture)

# 승진 기회 및 가능성 평점을 찾아 출력합니다.
promotion = driver.find_element(By.XPATH,
'//*[@id="premiumReviewStatistics"]/div/div[1]/div/div[2]/div[2]/div[4]/div/div[2]/span[2]').text
print('* 승진 기회 및 가능성 : ' + promotion)

# 경영진 평점을 찾아 출력합니다.
board = driver.find_element(By.XPATH,
'//*[@id="premiumReviewStatistics"]/div/div[1]/div/div[2]/div[2]/div[5]/div/div[2]/span[2]').text
print('* 경영진 : ' + board)
print('-'*100)