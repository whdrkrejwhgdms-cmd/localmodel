from pywinauto import Application, keyboard
import time

# UI 자동화 프레임워크인 pywinauto를 위한 Application 객체 생성
app = Application(backend='uia')

# C드라이브에 설치된 Notepad++ 실행 파일 경로 지정
notepad_exe_path = "C:\\Program Files\\Notepad++\\notepad++.exe"
# Notepad++ 실행
app.start(notepad_exe_path)

# Notepad++ 응용 프로그램 객체 가져오기
notepad = app['Notepad++']
# 2초 대기
time.sleep(2)

# 최대화 버튼 찾아 클릭
notepad.child_window(title="최대화", control_type="Button").click()
# 2초 대기
time.sleep(2)

# 메뉴 선택: 파일(F) -> 새 파일(N)
notepad.menu_select("파일(F)->새 파일(N)")
# 2초 대기
time.sleep(2)

# 편집기 창에서 안녕하세요 오토코더 입니다. 입력
notepad['Pane'].type_keys("안녕하세요 오토코더 입니다.{ENTER}", with_spaces=True)
notepad['Pane'].type_keys("앞으로 잘부탁드립니다.{ENTER}", with_spaces=True)
notepad['Pane'].type_keys("구독 좋아요 알람설정 부탁드립니다.", with_spaces=True)
# 2초 대기
time.sleep(2)

# 메뉴 선택: 파일(F) -> 저장(S)
notepad.menu_select("파일(F)->저장(S)")
# 2초 대기
time.sleep(2)

# 저장 창에서 Enter 키 누르기
keyboard.send_keys('{ENTER}')
# 2초 대기
time.sleep(2)

# Alt + F4 키 누르기 (프로그램 종료)
keyboard.send_keys('%{F4}')