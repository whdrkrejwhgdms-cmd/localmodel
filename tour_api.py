
import json
import html
import requests
import xml.etree.ElementTree as ET

from pathlib import Path
from urllib.parse import urlparse, parse_qs


# ==================================================
# 1. 기본 설정
# ==================================================

BASE_URL = "https://apis.data.go.kr/B551011/KorService2"

# 발급받은 일반 인증키(Decoding)를 입력하세요.
SERVICE_KEY = "U5i63xpIWM48raIRQBYpUXbA/wKd0iO6n/n1+JISyoEW1gWcEiz2No2fHPeid5TZoQN0HV85WyGv6LPwaQ8n4w=="

MOBILE_OS = "ETC"
MOBILE_APP = "TourInfoApp"

SAVE_DIR = Path("tour_data")
SAVE_DIR.mkdir(exist_ok=True)


# ==================================================
# 2. 코드 해석용 사전
# ==================================================

CONTENT_TYPES = {
    "12": "관광지",
    "14": "문화시설",
    "15": "행사·공연·축제",
    "25": "여행코스",
    "28": "레포츠",
    "32": "숙박",
    "38": "쇼핑",
    "39": "음식점",
}

REGION_CODES = {
    "11": "서울특별시",
    "26": "부산광역시",
    "27": "대구광역시",
    "28": "인천광역시",
    "29": "광주광역시",
    "30": "대전광역시",
    "31": "울산광역시",
    "36": "세종특별자치시",
    "41": "경기도",
    "42": "강원특별자치도",
    "43": "충청북도",
    "44": "충청남도",
    "45": "전북특별자치도",
    "46": "전라남도",
    "47": "경상북도",
    "48": "경상남도",
    "50": "제주특별자치도",
}

CATEGORY1_CODES = {
    "FD": "음식",
    "AD": "숙박",
    "AT": "관광지",
    "CT": "문화시설",
    "EX": "체험",
    "LS": "레포츠",
    "SH": "쇼핑",
}


# ==================================================
# 3. 공통 API 호출
# ==================================================

def call_api(operation, extra_params=None):
    if SERVICE_KEY == "여기에_발급받은_인증키_입력":
        print("먼저 SERVICE_KEY에 발급받은 인증키를 입력하세요.")
        return None

    params = {
        "serviceKey": SERVICE_KEY,
        "MobileOS": MOBILE_OS,
        "MobileApp": MOBILE_APP,
        "_type": "json",
        "numOfRows": 10,
        "pageNo": 1,
    }

    if extra_params:
        params.update(extra_params)

    url = f"{BASE_URL}/{operation}"

    print(f"\n[요청] {operation}")
    print("[안내] API 서버에 요청 중입니다.")

    try:
        response = requests.get(
            url,
            params=params,
            timeout=30,
        )

        print(f"[HTTP 상태] {response.status_code}")

        # HTTP 오류 응답도 본문을 확인해 API 오류 내용을 표시
        if response.status_code != 200:
            print("[HTTP 오류] 서버 응답에 문제가 있습니다.")
            print(response.text[:3000])
            save_text(
                f"{operation}_http_error.txt",
                response.text,
            )
            return None

        # JSON 우선 처리
        try:
            data = response.json()

        except ValueError:
            # 인증 오류 등이 XML로 반환되는 경우
            try:
                root = ET.fromstring(response.content)
                print("\n[XML 응답]")

                for element in root.iter():
                    if element.text and element.text.strip():
                        print(
                            f"{element.tag}: "
                            f"{element.text.strip()}"
                        )

                save_text(
                    f"{operation}_response.xml",
                    response.text,
                )

            except ET.ParseError:
                print("[오류] JSON과 XML 응답을 해석할 수 없습니다.")
                save_text(
                    f"{operation}_response.txt",
                    response.text,
                )

            return None

        # API의 JSON 응답은 response.header/body 구조
        api_response = data.get("response", data)
        header = api_response.get("header", {})

        result_code = str(header.get("resultCode", ""))
        result_msg = str(header.get("resultMsg", ""))

        if result_code and result_code != "0000":
            print(f"[API 오류 코드] {result_code}")
            print(f"[API 오류 내용] {result_msg}")

            save_json(
                f"{operation}_error.json",
                data,
            )
            return None

        print("[성공] API 응답을 받았습니다.")
        return data

    except requests.RequestException as e:
        print(f"[통신 오류] {e}")
        return None


# ==================================================
# 4. 파일 저장 함수
# ==================================================

def save_json(filename, data):
    path = SAVE_DIR / filename

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"[JSON 저장] {path.resolve()}")


def save_text(filename, content):
    path = SAVE_DIR / filename

    path.write_text(content, encoding="utf-8")

    print(f"[텍스트 저장] {path.resolve()}")


# ==================================================
# 5. API 결과 목록 추출
# ==================================================

def get_items(data):
    if not data:
        return []

    api_response = data.get("response", data)
    body = api_response.get("body", {})
    items = body.get("items", {}).get("item", [])

    if isinstance(items, dict):
        return [items]

    if isinstance(items, list):
        return items

    return []


def get_total_count(data):
    if not data:
        return 0

    api_response = data.get("response", data)
    return api_response.get("body", {}).get("totalCount", 0)


# ==================================================
# 전체 페이지 자동 수집
# ==================================================

def call_api_all(operation, extra_params=None, rows=100):
    all_items = []
    page_no = 1
    total_count = None
    first_data = None

    while True:
        print(f"\n[요청] {page_no}페이지 수집 중...")

        params = dict(extra_params or {})
        params["numOfRows"] = rows
        params["pageNo"] = page_no

        data = call_api(operation, params)

        if data is None:
            print("[중단] API 요청에 실패했습니다.")
            break

        if first_data is None:
            first_data = data
            total_count = int(get_total_count(data) or 0)
            print(f"[정보] 서버 전체 데이터: {total_count}건")

        items = get_items(data)

        if not items:
            print("[안내] 추가 데이터가 없습니다.")
            break

        all_items.extend(items)

        print(
            f"[진행] {page_no}페이지 완료 / "
            f"누적 {len(all_items)}건"
        )

        # 전체 데이터 수집 완료
        if len(all_items) >= total_count:
            break

        # 응답 데이터가 페이지 크기보다 적으면 마지막 페이지
        if len(items) < rows:
            break

        page_no += 1

    if first_data is None:
        return None

    # 첫 번째 응답의 구조를 유지하면서 전체 목록으로 교체
    result = dict(first_data)
    api_response = dict(result.get("response", result))
    body = dict(api_response.get("body", {}))

    body["items"] = {"item": all_items}
    body["totalCount"] = total_count
    body["numOfRows"] = len(all_items)

    api_response["body"] = body

    if "response" in result:
        result["response"] = api_response
    else:
        result = api_response

    print("\n[완료] 전체 페이지 수집 종료")
    print(f"[결과] 총 {len(all_items)}건 수집")

    return result



# ==================================================
# 6. 터미널 출력
# ==================================================

def print_results(data):
    items = get_items(data)

    if not items:
        print("[안내] 조회된 데이터가 없습니다.")
        return

    print(f"\n조회 결과: {len(items)}건")
    print("-" * 60)

    for index, item in enumerate(items, start=1):
        print(f"\n[{index}] {item.get('title', item.get('name', '이름 없음'))}")

        # 화면에서 우선 확인할 주요 항목
        fields = [
            "addr1",
            "addr2",
            "zipcode",
            "tel",
            "contentid",
            "contenttypeid",
            "areacode",
            "lDongRegnCd",
            "lDongSignguCd",
            "lclsSystm1",
            "lclsSystm2",
            "lclsSystm3",
            "firstimage",
            "mapx",
            "mapy",
        ]

        for field in fields:
            value = item.get(field)

            if value:
                print(f"{field}: {value}")

    print("-" * 60)


# ==================================================
# 7. HTML 생성
# ==================================================

# ==================================================
# HTML 이미지 갤러리 + 상세정보 화면
# 페이지당 20개 이미지 표시
# ==================================================

def save_html(data, filename="tour_info.html"):
    items = get_items(data)

    if not items:
        print("[안내] HTML로 저장할 데이터가 없습니다.")
        return

    cards = []
    details = []
    image_count = 0

    for item in items:
        # 추가 이미지가 있는 데이터만 갤러리에 표시
        image_url = str(item.get("firstimage2") or "").strip()

        if not image_url.startswith(("https://", "http://")):
            continue

        # 이미지 주소 검사
        from urllib.parse import urlparse
        parsed = urlparse(image_url)

        if not parsed.netloc:
            continue

        index = image_count
        image_count += 1

        title = str(item.get("title") or "이름 없음")
        address = str(item.get("addr1") or "주소 없음")
        content_id = str(item.get("contentid") or "-")

        safe_url = html.escape(image_url, quote=True)
        safe_title = html.escape(title)

        # 이미지 갤러리 카드
        cards.append(f"""
        <div class="image-card"
             data-index="{index}"
             onclick="showDetail({index})"
             tabindex="0"
             role="button"
             onkeydown="if(event.key==='Enter') showDetail({index})">

            <img src="{safe_url}"
                 alt="{safe_title}"
                 loading="lazy"
                 onerror="this.style.display='none';
                 this.nextElementSibling.style.display='flex'">

            <div class="image-error">이미지를 표시할 수 없습니다.</div>

            <div class="image-caption">
                <strong>{safe_title}</strong>
                <span>{html.escape(address)}</span>
            </div>
        </div>
        """)

        # 상세정보 표 생성
        rows = ""

        for key, value in item.items():
            display_value = str(value) if value not in (None, "") else "-"

            if key in ("firstimage", "firstimage2") and str(value).startswith(
                ("https://", "http://")
            ):
                safe_value = html.escape(str(value), quote=True)
                value_html = (
                    f'<a href="{safe_value}" target="_blank" '
                    f'rel="noopener">{html.escape(str(value))}</a>'
                )
            else:
                value_html = html.escape(display_value)

            rows += (
                f"<tr><th>{html.escape(str(key))}</th>"
                f"<td>{value_html}</td></tr>"
            )

        first_image = str(item.get("firstimage") or "").strip()
        first_image_html = ""

        if first_image.startswith(("https://", "http://")):
            first_image_html = f"""
            <div class="detail-image">
                <h3>대표 이미지</h3>
                <img src="{html.escape(first_image, quote=True)}"
                     alt="대표 이미지" loading="lazy">
            </div>
            """

        # 클릭한 이미지의 상세정보
        details.append(f"""
        <section class="detail-panel" id="detail-{index}"
                 style="display:none">

            <button class="back-button"
                    onclick="backToGallery()">
                ← 이미지 목록으로
            </button>

            <h2>{safe_title}</h2>

            <div class="detail-image">
                <h3>추가 이미지</h3>
                <img src="{safe_url}" alt="{safe_title}">
            </div>

            {first_image_html}

            <h3>주요 정보</h3>
            <table>
                <tr>
                    <th>관광지명</th>
                    <td>{safe_title}</td>
                </tr>
                <tr>
                    <th>주소</th>
                    <td>{html.escape(address)}</td>
                </tr>
                <tr>
                    <th>콘텐츠 ID</th>
                    <td>{html.escape(content_id)}</td>
                </tr>
                <tr>
                    <th>전화번호</th>
                    <td>{html.escape(str(item.get('tel') or '-'))}</td>
                </tr>
                <tr>
                    <th>우편번호</th>
                    <td>{html.escape(str(item.get('zipcode') or '-'))}</td>
                </tr>
                <tr>
                    <th>콘텐츠 유형</th>
                    <td>{html.escape(str(item.get('contenttypeid') or '-'))}</td>
                </tr>
                <tr>
                    <th>지역 코드</th>
                    <td>{html.escape(str(item.get('areacode') or '-'))}</td>
                </tr>
                <tr>
                    <th>법정동 시·도 코드</th>
                    <td>{html.escape(str(item.get('lDongRegnCd') or '-'))}</td>
                </tr>
                <tr>
                    <th>법정동 시·군·구 코드</th>
                    <td>{html.escape(str(item.get('lDongSignguCd') or '-'))}</td>
                </tr>
                <tr>
                    <th>위도</th>
                    <td>{html.escape(str(item.get('mapy') or '-'))}</td>
                </tr>
                <tr>
                    <th>경도</th>
                    <td>{html.escape(str(item.get('mapx') or '-'))}</td>
                </tr>
            </table>

            <details>
                <summary>전체 원본 데이터 보기</summary>
                <table>{rows}</table>
            </details>

            <details>
                <summary>원본 JSON 보기</summary>
                <pre>{html.escape(json.dumps(item, ensure_ascii=False, indent=2))}</pre>
            </details>
        </section>
        """)

    if image_count == 0:
        print("[안내] 추가 이미지(firstimage2)가 있는 데이터가 없습니다.")
        print("해당 API가 추가 이미지 URL을 제공하는지 확인하세요.")
        return

    document = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>관광정보 이미지 갤러리</title>

<style>
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 24px;
    font-family: Arial, "Malgun Gothic", sans-serif;
    background: #f1f5f9;
    color: #1e293b;
}}

header {{
    max-width: 1400px;
    margin: 0 auto 24px;
}}

h1 {{
    margin-bottom: 8px;
}}

.summary {{
    color: #64748b;
}}

.gallery {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
    max-width: 1400px;
    margin: 0 auto;
}}

.image-card {{
    background: white;
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 2px 10px #0001;
    transition: transform 0.15s;
}}

.image-card:hover {{
    transform: translateY(-3px);
}}

.image-card img {{
    display: block;
    width: 100%;
    height: 190px;
    object-fit: cover;
}}

.image-error {{
    display: none;
    height: 190px;
    align-items: center;
    justify-content: center;
    background: #e2e8f0;
    color: #64748b;
}}

.image-caption {{
    padding: 12px;
}}

.image-caption strong {{
    display: block;
    margin-bottom: 7px;
}}

.image-caption span {{
    display: block;
    font-size: 13px;
    color: #64748b;
    overflow-wrap: anywhere;
}}

.pagination {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 14px;
    margin: 28px auto;
}}

button {{
    border: 0;
    border-radius: 8px;
    padding: 10px 16px;
    cursor: pointer;
    background: #2563eb;
    color: white;
    font-size: 15px;
}}

button:disabled {{
    background: #cbd5e1;
    cursor: not-allowed;
}}

#page-info {{
    font-weight: bold;
}}

.detail-panel {{
    max-width: 900px;
    margin: 0 auto;
    padding: 24px;
    border-radius: 14px;
    background: white;
    box-shadow: 0 2px 10px #0001;
}}

.back-button {{
    margin-bottom: 20px;
}}

.detail-image {{
    margin: 20px 0;
}}

.detail-image img {{
    width: 100%;
    max-height: 480px;
    object-fit: contain;
    background: #f8fafc;
    border-radius: 8px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 24px;
    overflow-wrap: anywhere;
}}

th, td {{
    border-bottom: 1px solid #e2e8f0;
    padding: 10px;
    text-align: left;
    vertical-align: top;
}}

th {{
    width: 32%;
    background: #f8fafc;
}}

details {{
    margin: 18px 0;
    padding: 14px;
    background: #f8fafc;
    border-radius: 8px;
}}

summary {{
    cursor: pointer;
    font-weight: bold;
}}

pre {{
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}}

@media (max-width: 1000px) {{
    .gallery {{
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }}
}}

@media (max-width: 650px) {{
    body {{
        padding: 12px;
    }}

    .gallery {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 10px;
    }}

    .image-card img {{
        height: 140px;
    }}

    .detail-panel {{
        padding: 14px;
    }}
}}
</style>
</head>

<body>

<header id="gallery-header">
    <h1>관광정보 이미지 갤러리</h1>
    <div class="summary">
        추가 이미지 {image_count}개 · 페이지당 20개
    </div>
</header>

<main>
    <div id="gallery" class="gallery">
        {"".join(cards)}
    </div>

    <div id="pagination" class="pagination">
        <button id="prev" onclick="changePage(-1)">이전</button>
        <span id="page-info"></span>
        <button id="next" onclick="changePage(1)">다음</button>
    </div>

    <div id="detail-container" style="display:none">
        {"".join(details)}
    </div>
</main>

<script>
const pageSize = 20;
let currentPage = 1;

const cards = Array.from(
    document.querySelectorAll(".image-card")
);

const totalPages = Math.max(
    1, Math.ceil(cards.length / pageSize)
);

function renderPage() {{
    document.getElementById("gallery").style.display = "grid";
    document.getElementById("pagination").style.display = "flex";
    document.getElementById("gallery-header").style.display = "block";
    document.getElementById("detail-container").style.display = "none";

    cards.forEach((card, index) => {{
        const start = (currentPage - 1) * pageSize;
        card.style.display =
            index >= start && index < start + pageSize
            ? "block" : "none";
    }});

    document.getElementById("page-info").textContent =
        currentPage + " / " + totalPages + " 페이지";

    document.getElementById("prev").disabled =
        currentPage === 1;

    document.getElementById("next").disabled =
        currentPage === totalPages;

    window.scrollTo(0, 0);
}}

function changePage(direction) {{
    currentPage += direction;

    if (currentPage < 1) currentPage = 1;
    if (currentPage > totalPages) currentPage = totalPages;

    renderPage();
}}

function showDetail(index) {{
    document.getElementById("gallery").style.display = "none";
    document.getElementById("pagination").style.display = "none";
    document.getElementById("gallery-header").style.display = "none";
    document.getElementById("detail-container").style.display = "block";

    document.querySelectorAll(".detail-panel").forEach(panel => {{
        panel.style.display = "none";
    }});

    const selected = document.getElementById("detail-" + index);

    if (selected) {{
        selected.style.display = "block";
    }}

    window.scrollTo(0, 0);
}}

function backToGallery() {{
    document.getElementById("detail-container").style.display = "none";
    renderPage();
}}

renderPage();
</script>

</body>
</html>
"""

    path = SAVE_DIR / filename
    path.write_text(document, encoding="utf-8")

    print(f"\n[HTML 저장 완료] {path.resolve()}")
    print(f"[이미지 갤러리] 총 {image_count}개")
    print("[안내] HTML 파일을 브라우저에서 열어 확인하세요.")



# ==================================================
# 8. 공통 실행 및 저장
# ==================================================

def run_search(operation, params=None, filename="results"):
    data = call_api_all(
        operation,
        extra_params=params,
        rows=100
    )

    if data is None:
        return

    print_results(data)

    save_json(f"{filename}.json", data)
    save_html(data, f"{filename}.html")



# ==================================================
# 9. 메뉴별 조회
# ==================================================

def search_area_codes():
    run_search(
        "areaCode2",
        filename="area_codes",
    )


def search_keyword():
    keyword = input("검색 키워드: ").strip()

    if not keyword:
        print("키워드를 입력하세요.")
        return

    run_search(
        "searchKeyword2",
        {"keyword": keyword},
        "keyword_results",
    )


def search_area_based():
    print("법정동 시·도 코드 예: 서울 11, 부산 26")
    region = input("시·도 코드: ").strip()

    if not region:
        print("시·도 코드를 입력하세요.")
        return

    params = {"lDongRegnCd": region}

    sigungu = input(
        "시·군·구 코드 (모르면 Enter): "
    ).strip()

    if sigungu:
        params["lDongSignguCd"] = sigungu

    content_type = input(
        "콘텐츠 유형 코드 (전체는 Enter): "
    ).strip()

    if content_type:
        params["contentTypeId"] = content_type

    run_search(
        "areaBasedList2",
        params,
        "area_results",
    )


def search_festival():
    start_date = input(
        "행사 시작일 YYYYMMDD (예: 20261012): "
    ).strip()

    if not start_date.isdigit() or len(start_date) != 8:
        print("날짜를 YYYYMMDD 형식으로 입력하세요.")
        return

    run_search(
        "searchFestival2",
        {"eventStartDate": start_date},
        "festival_results",
    )


def search_stay():
    region = input(
        "법정동 시·도 코드 (서울 11, 부산 26): "
    ).strip()

    if not region:
        print("시·도 코드를 입력하세요.")
        return

    run_search(
        "searchStay2",
        {"lDongRegnCd": region},
        "stay_results",
    )


# ==================================================
# 10. 프로그램 시작
# ==================================================

def main():
    while True:
        print("\n" + "=" * 45)
        print(" 한국관광공사 국문 관광정보 조회 프로그램")
        print("=" * 45)
        print("1. 지역 코드 조회")
        print("2. 키워드 검색")
        print("3. 지역 기반 관광정보 조회")
        print("4. 행사 정보 조회")
        print("5. 숙박 정보 조회")
        print("0. 종료")

        menu = input("메뉴 선택: ").strip()

        if menu == "1":
            search_area_codes()

        elif menu == "2":
            search_keyword()

        elif menu == "3":
            search_area_based()

        elif menu == "4":
            search_festival()

        elif menu == "5":
            search_stay()

        elif menu == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("올바른 메뉴를 선택하세요.")


if __name__ == "__main__":
    main()