# 필요한 라이브러리 임포트
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys

# 키워드와 이미지 수량 입력 받기
keyword = input("크롤링 이미지 키워드를 입력하세요 : ")
number = int(input("크롤링 이미지 수량을 입력하세요 : "))

# 크롬 옵션 설정 및 브라우저 실행
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

# 구글 이미지 페이지 접속
driver.get('https://www.google.com/imghp?hl=ko&ogbl')

# 2초 대기
time.sleep(2)

# 검색창 찾기 및 키워드 입력 후 엔터
name = driver.find_element(By.CLASS_NAME, 'gLFyf')
name.send_keys(keyword)
time.sleep(2)
name.send_keys(Keys.ENTER)
time.sleep(2)

# 이미지 목록 찾기
images = driver.find_elements(By.XPATH, '//*[@id="islrg"]/div[1]/div')
# 크롤링된 이미지 URL 리스트
imageList = []

# 각 이미지 반복문
for i, image in enumerate(images):
    try:
        # 이미지 클릭
        image.click()
        time.sleep(1)

        # 확대된 이미지 주소 찾기
        print('-'*100)
        imageXPATH = '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]'
        imageURL = image.find_element(By.XPATH, imageXPATH).get_attribute('src')
        print(imageURL)
        time.sleep(1)

        # http로 시작하는 URL만 리스트에 추가
        if imageURL.startswith('http'):
            imageList.append(imageURL)

        # 필요한 이미지 수량까지 크롤링 후 종료
        if len(imageList) == number:
            break
    except Exception:
        pass

# 함수: 이미지 다운로드
def download_images(url, j):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    with open(f'C:\\AutoCoder\\{keyword}_{j}.jpg', 'wb') as file:
        file.write(response.content)

# 다운로드 함수 호출
for j, imageURL in enumerate(imageList, start=1):
    download_images(imageURL, j)