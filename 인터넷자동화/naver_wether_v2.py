import time
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from openpyxl import Workbook
import folium


# -----------------------------------
# 1. 지역 정보
# -----------------------------------

regions = {
    "서울": (37.5665, 126.9780),
    "부산": (35.1796, 129.0756),
    "대구": (35.8714, 128.6014),
    "인천": (37.4563, 126.7052),
    "광주": (35.1595, 126.8526),
    "대전": (36.3504, 127.3845),
    "울산": (35.5384, 129.3114),
    "제주": (33.4996, 126.5312)
}


# -----------------------------------
# 2. 웹브라우저 실행
# -----------------------------------

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

weather_data = []


# -----------------------------------
# 3. 지역별 날씨 가져오기
# -----------------------------------

def get_region_weather(region):

    print()
    print("=" * 40)
    print(region, "날씨 수집")
    print("=" * 40)

    query = quote(region + " 날씨")

    url = (
        "https://search.naver.com/search.naver"
        "?where=nexearch"
        "&sm=top_hty"
        "&fbm=0"
        "&ie=utf8"
        "&query=" + query
    )

    driver.get(url)

    # 오늘 날씨가 나타날 때까지 기다림
    wait.until(
        lambda d: len(
            d.find_elements(
                By.CSS_SELECTOR,
                "div._today"
            )
        ) > 0
    )

    soup = BeautifulSoup(
        driver.page_source,
        "html.parser"
    )

    today = soup.select_one("div._today")

    if today is None:
        print("날씨 정보를 찾지 못했습니다.")
        return

    # -----------------------------------
    # 현재 날씨
    # -----------------------------------

    current_weather = today.select_one(
        ".weather_main .blind"
    ).get_text(strip=True)

    current_temperature = today.select_one(
        ".temperature_text strong"
    ).get_text(" ", strip=True)


    # -----------------------------------
    # 미세먼지 / 초미세먼지
    # -----------------------------------

    dust = ""
    ultra_dust = ""

    for item in soup.select(
        "ul.today_chart_list > li.item_today"
    ):

        title = item.select_one(".title")
        value = item.select_one(".txt")

        if title is None or value is None:
            continue

        title = title.get_text(strip=True)
        value = value.get_text(strip=True)

        if title == "미세먼지":
            dust = value

        elif title == "초미세먼지":
            ultra_dust = value


    # -----------------------------------
    # 내일 최저 / 최고기온
    # -----------------------------------

    tomorrow_items = soup.select(
        "ul.weather_info_list._tomorrow > li"
    )

    min_temperature = ""
    max_temperature = ""
    rain_probability = ""

    for item in tomorrow_items:

        time_element = item.select_one(
            ".time_text"
        )

        temperature_element = item.select_one(
            ".temperature_text strong"
        )

        rain_element = item.select_one(
            "dl.summary_list dd.desc"
        )

        if (
            time_element is None
            or temperature_element is None
        ):
            continue

        time_text = time_element.get_text(
            " ",
            strip=True
        )

        future_temperature = temperature_element.get_text(
            " ",
            strip=True
        )

        if rain_element is not None:
            rain_value = rain_element.get_text(
                strip=True
            )
        else:
            rain_value = ""

        if "최저" in time_text:

            min_temperature = future_temperature

        elif "최고" in time_text:

            max_temperature = future_temperature
            rain_probability = rain_value


    # -----------------------------------
    # 데이터 저장
    # -----------------------------------

    data = {
        "지역": region,
        "현재날씨": current_weather,
        "현재기온": current_temperature,
        "최저기온": min_temperature,
        "최고기온": max_temperature,
        "강수확률": rain_probability,
        "미세먼지": dust,
        "초미세먼지": ultra_dust
    }

    weather_data.append(data)


    # -----------------------------------
    # 콘솔 출력
    # -----------------------------------

    print("지역 :", region)
    print("현재 날씨 :", current_weather)
    print("현재 기온 :", current_temperature)
    print("최저 기온 :", min_temperature)
    print("최고 기온 :", max_temperature)
    print("강수확률 :", rain_probability)
    print("미세먼지 :", dust)
    print("초미세먼지 :", ultra_dust)


# -----------------------------------
# 4. 모든 지역 날씨 수집
# -----------------------------------

for region in regions:

    get_region_weather(region)


# -----------------------------------
# 5. Excel 저장
# -----------------------------------

workbook = Workbook()

sheet = workbook.active
sheet.title = "지역날씨"


sheet.append([
    "지역",
    "현재날씨",
    "현재기온",
    "최저기온",
    "최고기온",
    "강수확률",
    "미세먼지",
    "초미세먼지"
])


for data in weather_data:

    sheet.append([
        data["지역"],
        data["현재날씨"],
        data["현재기온"],
        data["최저기온"],
        data["최고기온"],
        data["강수확률"],
        data["미세먼지"],
        data["초미세먼지"]
    ])


# 열 너비
widths = {
    "A": 12,
    "B": 15,
    "C": 12,
    "D": 12,
    "E": 12,
    "F": 12,
    "G": 12,
    "H": 14
}


for column, width in widths.items():

    sheet.column_dimensions[column].width = width


workbook.save("지역날씨.xlsx")


# -----------------------------------
# 6. Folium 지도 생성
# -----------------------------------

map_center = [36.5, 127.8]


# Esri 지도 타일
# OpenStreetMap 공식 타일 서버는 사용하지 않음
esri_tiles = (
    "https://services.arcgisonline.com/"
    "ArcGIS/rest/services/"
    "World_Street_Map/MapServer/tile/"
    "{z}/{y}/{x}"
)


esri_attribution = (
    "Tiles &copy; Esri | "
    "Sources: Esri, HERE, Garmin, USGS, "
    "Intermap, INCREMENT P, NRCan, "
    "Esri Japan, METI, Esri China (Hong Kong), "
    "Esri Korea, Esri (Thailand), NGCC, "
    "&copy; OpenStreetMap contributors, "
    "and the GIS User Community"
)


weather_map = folium.Map(

    location=map_center,

    zoom_start=7,

    tiles=esri_tiles,

    attr=esri_attribution
)


# -----------------------------------
# 7. 지역별 마커 추가
# -----------------------------------

for data in weather_data:

    region = data["지역"]

    latitude = regions[region][0]
    longitude = regions[region][1]


    # 팝업 내용
    popup_html = f"""
    <div style="width:230px;">

        <h3>{region}</h3>

        <b>날씨 :</b>
        {data["현재날씨"]}<br>

        <b>현재 기온 :</b>
        {data["현재기온"]}<br>

        <b>최저 기온 :</b>
        {data["최저기온"]}<br>

        <b>최고 기온 :</b>
        {data["최고기온"]}<br>

        <b>강수확률 :</b>
        {data["강수확률"]}<br>

        <b>미세먼지 :</b>
        {data["미세먼지"]}<br>

        <b>초미세먼지 :</b>
        {data["초미세먼지"]}

    </div>
    """


    # 지도에 마커 추가
    folium.Marker(

        location=[
            latitude,
            longitude
        ],

        tooltip=(
            region
            + " "
            + data["현재기온"]
        ),

        popup=folium.Popup(
            popup_html,
            max_width=300
        )

    ).add_to(weather_map)


# -----------------------------------
# 8. 지도 저장
# -----------------------------------

weather_map.save(
    "날씨지도.html"
)


# -----------------------------------
# 9. 종료
# -----------------------------------

driver.quit()


print()
print("=" * 40)
print("모든 작업이 완료되었습니다.")
print("=" * 40)
print()
print("Excel 파일 : 지역날씨.xlsx")
print("지도 파일  : 날씨지도.html")