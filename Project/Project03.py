import qrcode

# QR 코드 데이터가 담긴 파일 경로를 설정합니다.
QRcodeList = 'C:\\AutoCoder\\qrcodeList.txt'

# 파일을 읽기 모드로 열어서 각 줄의 데이터를 읽어옵니다.
with open(QRcodeList, 'r', encoding='UTF8') as f:
    lists = f.readlines()

    # 각 줄의 데이터에 대해 반복합니다.
    for item in lists:
        item = item.strip()  # 양 끝의 공백을 제거합니다.
        print(item)

        # QR 코드를 생성합니다.
        QR_Image = qrcode.make(item)

        # 도메인 이름을 추출하고, 첫 글자를 대문자로 만들어서 파일명으로 사용합니다.
        domain_name = item.split('.')[1].capitalize()

        # QR 코드 이미지를 저장할 파일 경로를 설정합니다.
        Image = f'C:\\AutoCoder\\QRCode\\{domain_name}.jpg'

        # QR 코드 이미지를 저장합니다.
        QR_Image.save(Image)