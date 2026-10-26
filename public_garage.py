import requests
import xml.etree.ElementTree as ET
import csv
import time

# 1. API 설정
URL = "https://apis.data.go.kr/B553774/Publicgarage/getPublicgarageQry"
SERVICE_KEY = "U5i63xpIWM48raIRQBYpUXbA/wKd0iO6n/n1+JISyoEW1gWcEiz2No2fHPeid5TZoQN0HV85WyGv6LPwaQ8n4w=="

CSV_FILE = "public_garage.csv"

# 한 페이지에서 조회할 데이터 수
NUM_OF_ROWS = 10


# 2. 페이지 데이터 요청
def get_page(page_no):

    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": page_no,
        "numOfRows": NUM_OF_ROWS
    }

    response = requests.get(
        URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    root = ET.fromstring(response.content)

    result_code = root.findtext(".//resultCode")
    result_msg = root.findtext(".//resultMsg")

    if result_code and result_code not in ("00", "0000"):
        raise Exception(
            f"API 오류: {result_code} - {result_msg}"
        )

    items = root.findall(".//item")

    total_count = root.findtext(".//totalCount")

    return items, total_count


# 3. 모든 페이지 수집
def get_all_public_garages():

    all_rows = []
    columns = []
    page_no = 1
    total_count = None

    print("=" * 50)
    print("버스 차고지 전체 데이터 수집 시작")
    print("=" * 50)

    try:
        while True:

            print(f"[요청] {page_no}페이지 수집 중...")

            items, count = get_page(page_no)

            if total_count is None and count is not None:
                total_count = int(count)
                print(f"[정보] 서버 전체 데이터: {total_count}건")

            # 데이터가 없으면 마지막 페이지로 판단
            if not items:
                print(f"[종료] {page_no}페이지에 데이터가 없습니다.")
                break

            for item in items:

                row = {}

                for child in item:
                    row[child.tag] = child.text or ""

                    if child.tag not in columns:
                        columns.append(child.tag)

                all_rows.append(row)

            print(
                f"[진행] {page_no}페이지 완료 / "
                f"누적 {len(all_rows)}건"
            )

            # 마지막 페이지에서 불필요한 요청을 줄임
            # if (
            #     total_count is not None
            #     and len(all_rows) >= total_count
            # ):
            #     print("[안내] 서버 전체 데이터 수집 완료")
            #     break

            page_no += 1

            # 서버에 과도한 요청이 발생하지 않도록 대기
            time.sleep(0.2)

        # 4. CSV 저장
        if not columns:
            print("[안내] 저장할 데이터가 없습니다.")
            return

        print("[저장] CSV 파일 작성 중...")

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=columns
            )

            writer.writeheader()
            writer.writerows(all_rows)

        print("=" * 50)
        print("전체 데이터 수집 및 저장 완료")
        print(f"수집한 페이지 수: {page_no}페이지")
        print(f"수집 건수: {len(all_rows)}건")
        print(f"CSV 파일: {CSV_FILE}")
        print("=" * 50)

    except requests.exceptions.RequestException as e:
        print(f"[오류] API 통신 실패: {e}")

    except ET.ParseError as e:
        print(f"[오류] XML 분석 실패: {e}")

    except Exception as e:
        print(f"[오류] 데이터 수집 실패: {e}")


# 5. 실행
if __name__ == "__main__":
    get_all_public_garages()