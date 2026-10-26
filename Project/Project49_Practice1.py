# smtplib 모듈은 SMTP 프로토콜을 사용하여 메일을 보내는데 필요한 기능을 제공합니다.
# email 모듈은 메일의 제목, 본문, 수신자, 첨부파일 등을 설정할 수 있습니다.
# 파일의 경로와 이름을 다루기 위해 os 모듈을 임포트합니다.
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os

# SMTP 서버의 URL과 포트 번호를 설정합니다.
smtp = smtplib.SMTP('smtp.gmail.com', 587)

# TLS 암호화를 시작합니다. (TLS 사용할 때에만 해당 코드 입력)
smtp.starttls()

# Gmail 계정의 아이디와 앱 비밀번호를 입력하여 로그인합니다.
smtp.login('devautocoder@gmail.com', 'dhbg lbrt ofst buqd')

# MIMEMultipart 객체를 생성합니다.
# MIMEMultipart 객체는 메일의 헤더와 본문, 첨부파일 등을 담을 수 있는 컨테이너입니다.
msg = MIMEMultipart()

# 메일의 제목, 발신자, 수신자를 설정합니다.
msg['Subject'] = '파이썬으로 Gmail 보내기'
msg['From'] = 'devautocoder@gmail.com'

# MIMEText 객체를 생성하고, attach 메서드를 사용하여 MIMEMultipart 객체에 추가합니다.
# MIMEText 객체는 메일의 본문을 텍스트 형식으로 작성할 수 있습니다.
msg.attach(MIMEText('이 메일은 파이썬으로 작성되었습니다.'))

# 수신자를 여러 명 지정하려면, 쉼표로 구분하여 메일 주소를 나열합니다.
# msg['To'] 에는 수신자의 메일 주소만 있는 리스트를 join 메서드를 사용하여 문자열로 변환합니다.
# sendmail 메서드에는 수신자의 메일 주소만 있는 리스트를 전달합니다.
recipients = ['autocoder@naver.com', 'lwjworld88@naver.com']
msg['To'] = ', '.join(recipients)

# 첨부파일의 경로와 이름을 리스트로 지정합니다.
attachments = [r"C:\AutoCoder\image1.jpg", r"C:\AutoCoder\image2.jpg"]

# 첨부파일 리스트를 반복문으로 순회하면서 MIMEApplication 객체를 생성하고 추가합니다.
# MIMEApplication 객체는 메일에 다양한 형식의 파일을 첨부할 수 있습니다.
for attachment in attachments:
    # 파일의 절대 경로를 입력하면, 두 가지 문자열을 나눠서 반환
    folder, file = os.path.split(attachment)
    # 첨부 파일을 열어서 내용을 가져옴
    with open(attachment, 'rb') as f:
        # 파일의 이름만 Name 매개변수로 전달
        msg.attach(MIMEApplication(f.read(), Name=file))

# 메일을 발송합니다.
smtp.sendmail('devautocoder@gmail.com', [email for email in recipients], msg.as_string())

# SMTP 서버와 연결을 종료합니다.
smtp.quit()