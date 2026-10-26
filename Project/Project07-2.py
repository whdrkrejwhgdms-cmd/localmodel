from faker import Faker
import csv

# Faker 라이브러리를 사용하여 한국어 가짜 데이터 생성
fake = Faker('ko-KR')

# CSV 파일을 쓰기 모드로 열고 writer 객체 생성
with open('C:/AutoCoder/sample_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    # CSV 파일의 헤더 작성
    writer.writerow(['이름', '주소', '전화번호', '이메일주소'])

    # 가짜 데이터를 생성하고 CSV 파일에 작성 (100개의 행)
    sample_data = [(fake.name(), fake.address(), fake.phone_number(), fake.email())
                   for i in range(100)]
    writer.writerows(sample_data)