# 시간 모듈과 웹 드라이버 설정에 필요한 모듈을 불러옵니다.
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# 사용자로부터 회사명을 입력받습니다.
keyword = input('회사명을 입력하세요 : ')

# 크롬 옵션을 설정하고 웹 드라이버를 초기화합니다.
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

# 입력받은 회사명을 이용하여 해당 회사의 리뷰 페이지로 이동합니다.
driver.get('https://www.teamblind.com/kr/company/{}/reviews'.format(keyword))
company = driver.find_element(By.CLASS_NAME, 'name').text

# 회사 정보를 출력합니다.
print('='*100)
print('회사 :', company)

# 전체 평점 정보를 추출하고 출력합니다.
totalRate = driver.find_element(By.XPATH,
'//*[@id="wrap"]/section/div/div/div[2]/div/div/div/div/section[1]/div/div[1]/div[1]/strong').text
totalScore = totalRate.split('\n')[-1]
print('전체 평점 :', totalScore)
print('='*100)

# 일정 시간 대기합니다.
time.sleep(5)

# 다양한 평가 항목에 대한 정보를 추출하고 출력합니다.
details = driver.find_element(By.CLASS_NAME, 'rating_cate')
detailScores = details.find_elements(By.TAG_NAME, 'li')

print('커리어 향상 :', detailScores[0].text.split(' ')[0])
print('업무와 삶의 균형 :', detailScores[1].text.split(' ')[0])
print('급여 및 복지 :', detailScores[2].text.split(' ')[0])
print('사내 문화 :', detailScores[3].text.split(' ')[0])
print('경영진 :', detailScores[4].text.split(' ')[0])
print('-'*100)