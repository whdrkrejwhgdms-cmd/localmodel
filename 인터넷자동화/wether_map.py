import time
from urllib.parse import quote
from urllib.request import urlopen
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

import folium


# ============================================================
# 1. 전국 시군구 행정구역 데이터 가져오기
# ============================================================

geojson_url = (
    "https://raw.githubusercontent.com/"
    "vuski/admdongkor/master/"
    "ver20260701/"
    "HangJeongDong_ver20260701.geojson"
)

print("전국 시군구 정보를 가져오는 중...")

with urlopen(geojson_url) as response:
    geojson = json.load(response)


# ============================================================
# 2. 좌표 추출 함수
# ============================================================

def get_all_points(coordinates):

    points = []

    if isinstance(coordinates, list):

        # [경도, 위도] 형태인지 확인
        if (
            len(coordinates) >= 2
            and isinstance(coordinates[0], (int, float))
            and isinstance(coordinates[1], (int, float))
        ):
            points.append(coordinates)

        else:
            for item in coordinates:
                points.extend(get_all_points(item))

    return points


# ============================================================
# 3. 시군구별 좌표 만들기
# ============================================================

region_points = {}


for feature in geojson["features"]:

    properties = feature["properties"]

    sido = properties.get("sidonm", "")
    sigungu = properties.get("sggnm", "")

    if not sido or not sigungu:
        continue

    region = sido + " " + sigungu

    geometry = feature.get("geometry")

    if not geometry:
        continue

    coordinates = geometry.get("coordinates", [])

    points = get_all_points(coordinates)

    if region not in region_points:
        region_points[region] = []

    region_points[region].extend(points)


# ============================================================
# 4. 시군구 대표 좌표 계산
# ============================================================

regions = {}


for region, points in region_points.items():

    if len(points) == 0:
        continue

    longitude = sum(
        point[0] for point in points
    ) / len(points)

    latitude = sum(
        point[1] for point in points
    ) / len(points)

    regions[region] = (
        latitude,
        longitude
    )


print()
print("시군구 개수 :", len(regions))
print()


# ============================================================
# 5. Selenium 실행
# ============================================================

options = webdriver.ChromeOptions()

# 브라우저를 화면에 표시
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 15)


# ============================================================
# 6. 날씨 데이터 저장
# ============================================================

weather_data = []

failed_regions = []


# ============================================================
# 7. 지역별 날씨 수집 함수
# ============================================================

def get_region_weather(region):

    print("=" * 40)
    print(f"{region} 날씨 수집")
    print("=" * 40)

    try:

        # ----------------------------------------------------
        # 세종시는 네이버 검색어를 별도로 처리
        # ----------------------------------------------------

        if region == "세종특별자치시 세종시":
            search_region = "세종특별자치시"

        else:
            search_region = region


        # ----------------------------------------------------
        # 네이버 날씨 검색
        # ----------------------------------------------------

        search_url = (
            "https://search.naver.com/search.naver?"
            "where=nexearch&query="
            + quote(search_region + " 날씨")
        )

        driver.get(search_url)


        # ----------------------------------------------------
        # 오늘 날씨 영역이 나타날 때까지 기다림
        # ----------------------------------------------------

        wait.until(
            lambda d: len(
                d.find_elements(
                    By.CSS_SELECTOR,
                    "div._today"
                )
            ) > 0
        )


        # ----------------------------------------------------
        # HTML 가져오기
        # ----------------------------------------------------

        soup = BeautifulSoup(
            driver.page_source,
            "html.parser"
        )


        today = soup.select_one(
            "div._today"
        )


        if today is None:
            raise Exception(
                "오늘 날씨 영역을 찾을 수 없습니다."
            )


        # ====================================================
        # 현재 날씨
        # ====================================================

        weather_element = today.select_one(
            "p.summary"
        )

        if weather_element:

            current_weather = (
                weather_element
                .get_text(" ", strip=True)
                .split()[-1]
            )

        else:

            current_weather = ""


        # ====================================================
        # 현재 기온
        # ====================================================

        temperature_element = today.select_one(
            "div.temperature_text"
        )

        if temperature_element:

            current_temperature = (
                temperature_element
                .get_text(" ", strip=True)
            )

            current_temperature = (
                current_temperature
                .replace("현재 온도", "")
                .strip()
            )

        else:

            current_temperature = ""


        # ====================================================
        # 내일 날씨
        # ====================================================

        tomorrow_items = soup.select(
            "ul.weather_info_list._tomorrow > li"
        )


        tomorrow_low = ""
        tomorrow_high = ""
        tomorrow_rain = ""


        for item in tomorrow_items:

            time_element = item.select_one(
                ".time_text"
            )

            if not time_element:
                continue

            time_text = time_element.get_text(
                " ",
                strip=True
            )


            # ------------------------------------------------
            # 오전 최저기온
            # ------------------------------------------------

            if "오전" in time_text:

                temperature = item.select_one(
                    ".temperature_text strong"
                )

                if temperature:

                    tomorrow_low = (
                        temperature
                        .get_text(" ", strip=True)
                    )


                rain = item.select_one(
                    "dl.summary_list dd.desc"
                )

                if rain:

                    tomorrow_rain = (
                        rain.get_text(
                            " ",
                            strip=True
                        )
                    )


            # ------------------------------------------------
            # 오후 최고기온
            # ------------------------------------------------

            elif "오후" in time_text:

                temperature = item.select_one(
                    ".temperature_text strong"
                )

                if temperature:

                    tomorrow_high = (
                        temperature
                        .get_text(" ", strip=True)
                    )


        # ====================================================
        # 미세먼지 / 초미세먼지
        # ====================================================

        pm10 = ""
        pm25 = ""


        dust_items = soup.select(
            "ul.today_chart_list > li.item_today"
        )


        for item in dust_items:

            title = item.select_one(
                ".title"
            )

            if not title:
                continue

            title_text = title.get_text(
                " ",
                strip=True
            )


            value = item.select_one(
                ".txt"
            )

            if not value:
                continue

            value_text = value.get_text(
                " ",
                strip=True
            )


            if "미세먼지" in title_text and "초미세먼지" not in title_text:

                pm10 = value_text


            elif "초미세먼지" in title_text:

                pm25 = value_text


        # ====================================================
        # 결과 출력
        # ====================================================

        print(
            "날씨      :",
            current_weather
        )

        print(
            "현재기온  :",
            current_temperature
        )

        print(
            "내일 최저 :",
            tomorrow_low
        )

        print(
            "내일 최고 :",
            tomorrow_high
        )

        print(
            "강수확률  :",
            tomorrow_rain
        )

        print(
            "미세먼지  :",
            pm10
        )

        print(
            "초미세먼지:",
            pm25
        )


        # ====================================================
        # 데이터 저장
        # ====================================================

        data = {

            "지역": region,

            "날씨": current_weather,

            "현재기온": current_temperature,

            "내일최저": tomorrow_low,

            "내일최고": tomorrow_high,

            "강수확률": tomorrow_rain,

            "미세먼지": pm10,

            "초미세먼지": pm25
        }


        return data


    # ========================================================
    # TimeoutException
    # ========================================================

    except TimeoutException:

        print()
        print(
            "[실패] 시간 초과 :",
            region
        )

        failed_regions.append(region)

        return None


    # ========================================================
    # 기타 오류
    # ========================================================

    except Exception as e:

        print()
        print(
            "[오류]",
            region
        )

        print(
            "오류 내용 :",
            e
        )

        failed_regions.append(region)

        return None


# ============================================================
# 8. 전국 시군구 날씨 수집
# ============================================================

total_count = len(regions)

current_count = 0


for region in regions:

    current_count += 1

    print()
    print(
        f"[{current_count}/{total_count}]"
    )

    data = get_region_weather(region)


    # --------------------------------------------------------
    # 정상적으로 수집된 경우만 저장
    # --------------------------------------------------------

    if data is not None:

        weather_data.append(data)


    # --------------------------------------------------------
    # 다음 지역 요청 전 잠시 대기
    # --------------------------------------------------------

    time.sleep(1)


# ============================================================
# 9. 브라우저 종료
# ============================================================

driver.quit()


# ============================================================
# 10. 수집 결과 확인
# ============================================================

print()
print("=" * 50)
print("날씨 수집 완료")
print("=" * 50)

print(
    "전체 지역 :",
    total_count
)

print(
    "성공 지역 :",
    len(weather_data)
)

print(
    "실패 지역 :",
    len(failed_regions)
)


# ============================================================
# 11. 실패 지역 출력
# ============================================================

if failed_regions:

    print()
    print("=" * 50)
    print("수집 실패 지역")
    print("=" * 50)

    for region in failed_regions:

        print(
            "-",
            region
        )

else:

    print()
    print("모든 지역 수집 성공!")


# ============================================================
# 12. Folium 지도 생성
# ============================================================

map_center = [
    36.5,
    127.8
]


# 기존에 정상 동작했던 Esri 지도
esri_tiles = (
    "https://services.arcgisonline.com/"
    "ArcGIS/rest/services/"
    "World_Street_Map/MapServer/tile/"
    "{z}/{y}/{x}"
)

esri_attribution = (
    "Tiles © Esri"
)


weather_map = folium.Map(

    location=map_center,

    zoom_start=7,

    tiles=esri_tiles,

    attr=esri_attribution
)


# ============================================================
# 13. 날씨 정보를 지도에 표시
# ============================================================

for data in weather_data:

    region = data["지역"]


    if region not in regions:
        continue


    latitude, longitude = regions[region]


    # --------------------------------------------------------
    # 팝업 내용
    # --------------------------------------------------------

    popup_html = f"""
    <div style="width:250px">

        <h4>{region}</h4>

        <hr>

        <b>현재 날씨</b> :
        {data["날씨"]}<br>

        <b>현재 기온</b> :
        {data["현재기온"]}<br>

        <b>내일 최저</b> :
        {data["내일최저"]}<br>

        <b>내일 최고</b> :
        {data["내일최고"]}<br>

        <b>강수확률</b> :
        {data["강수확률"]}<br>

        <b>미세먼지</b> :
        {data["미세먼지"]}<br>

        <b>초미세먼지</b> :
        {data["초미세먼지"]}

    </div>
    """


    # --------------------------------------------------------
    # 지도 마커
    # --------------------------------------------------------

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


# ============================================================
# 14. 지도 저장
# ============================================================

weather_map.save(
    "전국시군구날씨지도.html"
)


print()
print("=" * 50)
print("지도 생성 완료")
print("=" * 50)

print(
    "전국시군구날씨지도.html"
)

print()
print("프로그램 종료")