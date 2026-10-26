# smtplib과 email 라이브러리를 임포트합니다.
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
# os 모듈을 임포트합니다.
import os

# 메일을 보내는 함수를 정의합니다.
def send_mail(sender, receiver, subject, content, file_name):
    # 메일 객체를 생성하고, 헤더를 설정합니다.
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    # 메일 본문을 MIMEText 객체로 생성하고, 메일 객체에 첨부합니다.
    text = MIMEText(content, "plain")
    msg.attach(text)

    # 파일의 확장자를 구합니다.
    extension = os.path.splitext(file_name)[-1].lower()

    # 파일의 확장자에 따라 서브타입을 결정합니다.
    if extension == ".jpg":
        subtype = "jpeg"
    elif extension == ".png":
        subtype = "png"
    # ... 생략 ...
    else:
        subtype = "unknown"

    # 파일을 바이너리 모드로 열고, MIMEImage 객체로 생성합니다.
    with open(file_name, "rb") as f:
        image = MIMEImage(f.read(), _subtype=subtype)

    # 이미지 객체에 Content-Disposition 헤더를 추가합니다.
    # 이 헤더는 첨부파일의 이름과 다운로드 여부를 설정합니다.
    # inline은 이미지가 본문에 나타나게 하고, attachment는 다운로드하게 합니다.
    image.add_header("Content-Disposition", "inline", filename=file_name)

    # 이미지 객체를 메일 객체에 첨부합니다.
    msg.attach(image)

    # 네이버 smtp 서버에 접속하고, 로그인하고, 메일을 보냅니다.
    # 네이버 smtp 서버 주소는 smtp.naver.com이고, 포트 번호는 587입니다.
    # 로그인할 때는 네이버 아이디와 보안 비밀번호를 사용합니다.
    server = smtplib.SMTP("smtp.naver.com", 587)
    server.starttls()
    server.login(sender, "비밀번호")
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

    # 메일 발송이 완료되었음을 반환합니다.
    return "메일 발송이 완료되었습니다."