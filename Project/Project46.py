from bs4 import BeautifulSoup
import requests
import os

def download_images(query, num_images):
    base_url = "https://www.google.co.in"
    url = base_url + "/search?q=" + query + "&source=lnms&tbm=isch"
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Google 이미지 검색 결과를 가져옵니다.
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 이미지 태그를 찾습니다.
    images = soup.find_all('img')

    # 지정된 수만큼 이미지를 다운로드합니다.
    for i, img in enumerate(images[:num_images+1]):
        img_url = img['src']

        # 이미지 URL이 'http'로 시작하지 않으면 전체 URL로 변경합니다.
        if not img_url.startswith('http'):
            img_url = base_url + img_url

        # 이미지를 다운로드하고 저장합니다.
        response = requests.get(img_url)
        with open(f'C:\\AutoCoder\\{query}_{i}.jpg', 'wb') as file:
            file.write(response.content)

    # 첫 번째 이미지를 삭제합니다.
    os.remove(f'C:\\AutoCoder\\{query}_0.jpg')

# '아이유'라는 검색어로 10개의 이미지를 다운로드합니다.
download_images('BTS', 10)