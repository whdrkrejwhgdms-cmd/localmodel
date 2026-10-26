import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from openpyxl import Workbook


# -----------------------------------
# 브라우저 실행
# -----------------------------------
driver = webdriver.Chrome()

url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%82%A0%EC%94%A8"

driver.get(url)

wait = WebDriverWait(driver, 10)


# -----------------------------------
# 날씨 데이터를 저장할 리스트
# -----------------------------------
weather_data = []


# -----------------------------------
# 오늘 날씨
# -----------------------------------
def get_today_weather():

    soup = BeautifulSoup(driver.page_source, "html.parser")

    today = soup.select_one("div._today")

    # 현재 날씨
    weather = today.select_one(
        ".weather_main .blind"
    ).get_text(strip=True)

    # 현재 온도
    temperature = today.select_one(
        ".temperature_text strong"
    ).get_text(" ", strip=True)

    # 어제와 비교
    summary = today.select_one(
        ".temperature_info p.summary"
    )

    yesterday = summary.select_one(
        ".temperature"
    ).get_text(" ", strip=True)

    yesterday_weather = summary.select_one(
        ".weather"
    ).get_text(strip=True)

    # 체감 / 습도 / 바람
    details = {}

    for item in today.select("dl.summary_list .sort"):

        title = item.select_one(".term").get_text(strip=True)
        value = item.select_one(".desc").get_text(strip=True)

        details[title] = value

    # 미세먼지 / 초미세먼지 / 자외선 / 일출
    dust = ""
    ultra_dust = ""
    uv = ""
    sunrise = ""

    for item in soup.select("ul.today_chart_list > li.item_today"):

        title = item.select_one(".title").get_text(strip=True)
        value = item.select_one(".txt").get_text(strip=True)

        if title == "미세먼지":
            dust = value

        elif title == "초미세먼지":
            ultra_dust = value

        elif title == "자외선":
            uv = value

        elif title == "일출":
            sunrise = value

    # 화면 출력
    print()
    print("=" * 60)
    print("                         오늘 날씨")
    print("=" * 60)

    print()
    print("[현재 날씨]")
    print("날씨       :", weather)
    print("현재 온도  :", temperature)
    print("어제 비교  :", yesterday, yesterday_weather)
    print("체감       :", details.get("체감", ""))
    print("습도       :", details.get("습도", ""))
    print("바람       :", details.get("서풍", ""))
    print("미세먼지   :", dust)
    print("초미세먼지 :", ultra_dust)
    print("자외선     :", uv)
    print("일출       :", sunrise)

    # 엑셀 저장용 데이터
    weather_data.append([
        "오늘",
        "현재",
        weather,
        temperature,
        yesterday + " " + yesterday_weather,
        details.get("체감", ""),
        details.get("습도", ""),
        details.get("서풍", ""),
        "",
        dust,
        ultra_dust,
        uv,
        sunrise
    ])


# -----------------------------------
# 내일 / 모레 날씨
# -----------------------------------
def get_future_weather(day):

    # 내일과 모레는 HTML 구조가 다름
    if day == "내일":
        selector = "ul.weather_info_list._tomorrow > li"
    else:
        selector = "ul.weather_info_list._after_tomorrow > li"

    # 오전 / 오후 2개가 나올 때까지 기다림
    wait.until(
        lambda d: len(
            d.find_elements(By.CSS_SELECTOR, selector)
        ) >= 2
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")

    items = soup.select(selector)

    print()
    print("=" * 60)
    print(f"                         {day} 날씨")
    print("=" * 60)

    for item in items:

        # 오전 / 오후
        time_text = item.select_one(
            ".time_text"
        ).get_text(" ", strip=True)

        # 날씨
        weather = item.select_one(
            ".weather_main .blind"
        ).get_text(strip=True)

        # 온도
        temperature = item.select_one(
            ".temperature_text strong"
        ).get_text(" ", strip=True)

        # 강수확률
        rain = item.select_one(
            "dl.summary_list dd.desc"
        ).get_text(strip=True)

        # 미세먼지
        dust = ""

        # 초미세먼지
        ultra_dust = ""

        for dust_item in item.select(
            "ul.today_chart_list > li"
        ):

            title = dust_item.select_one(
                ".title"
            ).get_text(strip=True)

            value = dust_item.select_one(
                ".txt"
            ).get_text(strip=True)

            if "미세" in title and "초미세" not in title:
                dust = value

            elif "초미세" in title:
                ultra_dust = value

        # 화면 출력
        print()
        print(f"[{time_text}]")
        print("날씨       :", weather)
        print("예측 온도  :", temperature)
        print("강수확률   :", rain)
        print("미세먼지   :", dust)
        print("초미세먼지 :", ultra_dust)

        # 엑셀 저장
        weather_data.append([
            day,
            time_text,
            weather,
            temperature,
            "",
            "",
            "",
            "",
            rain,
            dust,
            ultra_dust,
            "",
            ""
        ])


# -----------------------------------
# 1. 오늘
# -----------------------------------
get_today_weather()


# -----------------------------------
# 2. 내일
# -----------------------------------
tomorrow = wait.until(
    lambda d: d.find_element(
        By.XPATH,
        "//a[span[contains(@class, 'menu') and normalize-space()='내일']]"
    )
)

tomorrow.click()

# 데이터 변경 대기
time.sleep(5)

get_future_weather("내일")


# -----------------------------------
# 3. 모레
# -----------------------------------
day_after = wait.until(
    lambda d: d.find_element(
        By.XPATH,
        "//a[span[contains(@class, 'menu') and normalize-space()='모레']]"
    )
)

day_after.click()

# 데이터 변경 대기
time.sleep(5)

get_future_weather("모레")


# -----------------------------------
# 4. 엑셀 파일 생성
# -----------------------------------
workbook = Workbook()

sheet = workbook.active

sheet.title = "날씨정보"


# -----------------------------------
# 엑셀 제목
# -----------------------------------
sheet.append([
    "날짜",
    "시간",
    "날씨",
    "온도",
    "어제대비",
    "체감온도",
    "습도",
    "바람",
    "강수확률",
    "미세먼지",
    "초미세먼지",
    "자외선",
    "일출"
])


# -----------------------------------
# 데이터 입력
# -----------------------------------
for data in weather_data:
    sheet.append(data)


# -----------------------------------
# 열 너비 설정
# -----------------------------------
widths = {
    "A": 10,
    "B": 18,
    "C": 12,
    "D": 15,
    "E": 18,
    "F": 12,
    "G": 10,
    "H": 12,
    "I": 12,
    "J": 12,
    "K": 14,
    "L": 10,
    "M": 10
}

for column, width in widths.items():
    sheet.column_dimensions[column].width = width


# -----------------------------------
# 엑셀 저장
# -----------------------------------
filename = "날씨정보.xlsx"

workbook.save(filename)


print()
print("=" * 60)
print("                 엑셀 저장 완료")
print("=" * 60)
print()
print("파일명 :", filename)
print()


# -----------------------------------
# 브라우저 종료
# -----------------------------------
driver.quit()