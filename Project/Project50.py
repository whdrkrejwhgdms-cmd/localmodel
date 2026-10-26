# 필요한 모듈 임포트하기
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# 사용자로부터 키워드를 입력받기
keyword = input('나라장터에서 정보를 확인할 키워드를 입력해주세요 : ')

# 크롬 옵션 객체 생성하기
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

# 나라장터 웹사이트에 접속하기
driver.get('https://www.g2b.go.kr/index.jsp')
time.sleep(2)

# 검색어 입력란에 키워드 입력하기
driver.find_element(By.ID, 'bidNm').send_keys(keyword)
time.sleep(2)

# '검색' 단추 클릭하기
driver.find_element(By.CLASS_NAME, 'fr').click()
time.sleep(5)

# 프레임 살펴보기 (frame 태그 이름 확인하기)
iframes = driver.find_elements(By.CSS_SELECTOR, 'frame')

# frame 태그에서 본문 내용이 있는 'sub' frame으로 전환하기
driver.switch_to.frame('sub')

# frame 태그에서 본문 내용이 있는 'main' frame으로 전환하기
driver.switch_to.frame('main')

# 본문 내용이 있는 영역으로 이동하기
results = driver.find_element(By.CLASS_NAME, 'results')
body = results.find_element(By.TAG_NAME, 'tbody')
contents = body.find_elements(By.TAG_NAME, 'tr')

# CSV 파일에 저장할 데이터 헤더값 준비하기
data = [
    ['업무', '공고번호-차수', '분류', '공고명',
     '공고기관', '수요기관', '계약방법', '마감일시', '공동수급', '투찰']
]

for content in contents:
    items = content.find_elements(By.TAG_NAME, 'td')
    # CSV 파일에 업데이트할 데이터 추출하기
    task = items[0].text.strip()
    noticeNumber = items[1].text.strip()
    category = items[2].text.strip()
    description = items[3].text.strip()
    announcementAgency = items[4].text.strip()
    demandAgency = items[5].text.strip()
    contract = items[6].text.strip()
    deadline = items[7].text.strip()
    jointSupplyDemand = items[8].text.strip()
    bid = items[9].text.strip()

    # 데이터 리스트에 각 행의 데이터 추가하기
    data.append([
        task, noticeNumber, category, description,
        announcementAgency, demandAgency, contract,
        deadline, jointSupplyDemand, bid
    ])

# CSV파일 열고, csv.writer 객체 생성하기
with open('C:\\AutoCoder\\narajangtu.csv', 'w', encoding='ANSI', newline='') as f:
    writer = csv.writer(f)

    # 데이터 리스트의 각 요소를 CSV파일의 한 행으로 쓰기
    for row in data:
        writer.writerow(row)

# 크롤링 완료되었다는 결과를 출력합니다.
print("나라장터에서 키워드 정보를 모두 추출하였습니다.")

# 메일 발송 함수를 호출합니다.
from Project50_SMTP import send_mail
# 보내는 사람, 받는 사람, 제목, 내용, 첨부파일을 설정합니다.
sender = "autocoder@naver.com"
receiver = "devautocoder@gmail.com"
subject = f"나라장터에서 {keyword} 추출 정보입니다."
content = "이 메일은 파이썬에 의해 자동으로 발송되는 정보입니다."
file_name = "C:\\AutoCoder\\narajangtu.csv"

# send_mail 함수를 호출하고, 결과를 출력합니다.
result = send_mail(sender, receiver, subject, content, file_name)
print(result)