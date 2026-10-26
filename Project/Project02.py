# pyautogui 라이브러리와 time 라이브러리를 임포트합니다.
import pyautogui
import time

while True:
    # 마우스를 x=366, y=215 위치로 2초 동안 이동시킵니다.
    pyautogui.moveTo(366, 215, 2)

    # 5초 동안 대기합니다.
    time.sleep(5)

    # 마우스를 x=606, y=385 위치로 2초 동안 이동시킵니다.
    pyautogui.moveTo(606, 385, 2)

    # 5초 동안 대기합니다.
    time.sleep(5)