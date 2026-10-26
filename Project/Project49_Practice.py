# smtplib와 email 모듈을 임포트합니다.
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
msg = MIMEMultipart()

# 메일의 제목, 본문, 발신자, 수신자를 설정합니다.
msg['Subject'] = '파이썬으로 Gmail 보내기'
msg['From'] = 'devautocoder@gmail.com'
msg.attach(MIMEText('내용 : 본문 내용'))

# 수신자를 여러 명 지정하려면, 쉼표로 구분하여 메일 주소를 나열합니다.
# msg['To'] 에는 수신자의 이름과 메일 주소를 튜플로 묶은 리스트를 join 메서드를 사용하여 문자열로 변환합니다.
# sendmail 메서드에는 수신자의 메일 주소만 있는 리스트를 전달합니다.
# recipients = [('AutoCoder', 'autocoder@naver.com'), ('LWJ', 'lwjworld88@naver.com')]
recipients = ['autocoder@naver.com', 'lwjworld88@naver.com']
# msg['To'] = ', '.join('{} <{}>'.format(name, email) for name, email in recipients)
msg['To'] = ', '.join(recipients)


# 첨부파일의 경로와 이름을 리스트로 지정합니다.
attachments = [r"C:\AutoCoder\image1.jpg", r"C:\AutoCoder\image2.jpg"]

# 첨부파일 리스트를 반복문으로 순회하면서 MIMEApplication 객체를 생성하고 추가합니다.
for attachment in attachments:
    folder, file = os.path.split(attachment) # 파일의 절대 경로를 입력하면, 두 가지 문자열을 나눠서 반환
    with open(attachment, 'rb') as f: # 첨부 파일을 열어서 내용을 가져옴
        msg.attach(MIMEApplication(f.read(), Name=file)) # 파일의 이름만 Name 매개변수로 전달

# 메일을 발송합니다.
smtp.sendmail('devautocoder@gmail.com', [email for email in recipients], msg.as_string())

# SMTP 서버와 연결을 종료합니다.
smtp.quit()
