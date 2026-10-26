from faker import Faker

# 한국어 가짜 데이터 생성을 위해 Faker 객체 생성
fake = Faker('ko-KR')

# 가짜 이름 출력
print("가짜 이름:", fake.name())

# 가짜 주소 출력
print("가짜 주소:", fake.address())

# 가짜 전화번호 출력
print("가짜 전화번호:", fake.phone_number())

# 가짜 이메일 주소 출력
print("가짜 이메일 주소:", fake.email())
