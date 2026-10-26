from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup


# ---------------------------------
# 수집할 지역
# ---------------------------------

regions = [
    "서울특별시 종로구",
    "서울특별시 중구",
    "서울특별시 용산구",
    "부산광역시 중구",
    "대구광역시 중구"
]


# ---------------------------------
# 크롬 실행
# ---------------------------------

driver = webdriver.Chrome()


# ---------------------------------
# 지역별 날씨 수집
# ---------------------------------

for region in regions:

    print()
    print("수집 중 :", region)

    # 네이버 검색 주소
    url = (
        "https://search.naver.com/search.naver?"
        "where=nexearch&query=" + quote(region + " 날씨")
    )

    # 네이버 접속
    driver.get(url)

    # 날씨 영역이 나타날 때까지 기다리기
    WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "div._today")
    )

    # HTML 가져오기
    html = driver.page_source

    # HTML 분석
    soup = BeautifulSoup(html, "html.parser")

    # 현재 날씨 영역
    today = soup.select_one("div._today")


    # ---------------------------------
    # 현재 기온
    # ---------------------------------

    temperature = today.select_one("div.temperature_text")

    if temperature:
        temperature = temperature.get_text(" ", strip=True)
        temperature = temperature.replace("현재 온도", "").strip()
    else:
        temperature = "확인 안됨"


    # ---------------------------------
    # 현재 날씨
    # ---------------------------------

    weather = today.select_one("p.summary")

    if weather:
        weather = weather.get_text(" ", strip=True)

        # 현재 구조에서는 마지막 단어가 날씨 상태
        weather = weather.split()[-1]
    else:
        weather = "확인 안됨"


    # ---------------------------------
    # 결과 출력
    # ---------------------------------

    print("지역 :", region)
    print("날씨 :", weather)
    print("기온 :", temperature)


# ---------------------------------
# 크롬 종료
# ---------------------------------

driver.quit()