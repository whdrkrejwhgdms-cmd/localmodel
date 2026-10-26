# smtplib과 email 라이브러리를 임포트합니다.
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# 보내는 사람, 받는 사람, 제목, 내용, 첨부파일을 설정합니다.
sender = "autocoder@naver.com"
receiver = "devautocoder@gmail.com"
subject = "네이버 smtp 메일 발송 테스트"
content = "이 메일은 파이썬으로 작성되었습니다."
file_name = "C:\\AutoCoder\\image.jpg"

# 메일 객체를 생성하고, 헤더를 설정합니다.
msg = MIMEMultipart()
msg["From"] = sender
msg["To"] = receiver
msg["Subject"] = subject

# 메일 본문을 MIMEText 객체로 생성하고, 메일 객체에 첨부합니다.
text = MIMEText(content, "plain")
msg.attach(text)

# 이미지 파일을 바이너리 모드로 열고, MIMEImage 객체로 생성합니다.
with open(file_name, "rb") as f:
    image = MIMEImage(f.read())

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
server.login("보내는사람 메일주소", "비밀번호")
server.sendmail(sender, receiver, msg.as_string())
server.quit()

# 메일 발송이 완료되었음을 출력합니다.
print("메일 발송이 완료되었습니다.")